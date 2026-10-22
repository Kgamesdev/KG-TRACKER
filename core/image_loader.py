"""Gestor de descarga y caché asíncrona de miniaturas para KG Tracker con seguridad de red (SEC-03)."""

import os
import hashlib
import time
from urllib.parse import urlsplit
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool, Qt
from PySide6.QtGui import QImage, QPixmap

from core.paths import CACHE_DIR
from core.network import descargar_contenido_seguro
from logger import log_error, log_warning


class _ImageWorkerSignals(QObject):
    completado = Signal(str, QImage)


class _ImageDownloadWorker(QRunnable):
    """Worker que descarga y cachea la imagen en un hilo secundario de forma aislada e independiente."""

    def __init__(self, url: str, ruta_disco: str, target_size: tuple = (190, 104)):
        super().__init__()
        self.url = url
        self.ruta_disco = ruta_disco
        self.target_size = target_size
        self.signals = _ImageWorkerSignals()

    def run(self):
        try:
            # Reintentar una vez los fallos transitorios de red o decodificación.
            # La espera ocurre en el worker para no bloquear el hilo de la interfaz.
            for intento in range(2):
                contenido = descargar_contenido_seguro(self.url)
                if contenido:
                    img = QImage()
                    if img.loadFromData(contenido):
                        try:
                            img.save(self.ruta_disco, "PNG")
                        except Exception as error:
                            log_error(f"No se pudo cachear una miniatura: {error}")

                        scaled = img.scaled(
                            self.target_size[0],
                            self.target_size[1],
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                        self.signals.completado.emit(self.url, scaled)
                        return
                if intento == 0:
                    time.sleep(0.4)

            host = urlsplit(self.url).hostname or "desconocido"
            log_warning(f"No se pudo cargar la miniatura desde {host} tras 2 intentos.")
        except Exception as error:
            # Una excepción no puede escapar de QRunnable.run(): PySide puede
            # terminar el proceso si cruza la frontera C++/Python.
            log_error(f"Error inesperado descargando miniatura: {error}", exc_info=True)

        self.signals.completado.emit(self.url, QImage())


class ImageLoader(QObject):
    """Singleton coordinador de carga de imágenes con doble caché (RAM + Disco)."""

    _instancia = None

    @classmethod
    def get_instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        super().__init__()
        os.makedirs(CACHE_DIR, exist_ok=True)
        self._ram_cache = {}          
        self._descargas_en_curso = {}  
        self._workers = {}
        self._pool = QThreadPool.globalInstance()

    def _ruta_cache(self, url: str) -> str:
        hash_url = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return os.path.join(CACHE_DIR, f"{hash_url}.png")

    def cargar(self, url: str, callback, target_size: tuple = (190, 104)):
        if not url:
            callback(url, None)
            return

        if url in self._ram_cache:
            callback(url, self._ram_cache[url])
            return

        ruta = self._ruta_cache(url)
        if os.path.exists(ruta):
            pixmap = QPixmap(ruta)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    target_size[0],
                    target_size[1],
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self._ram_cache[url] = scaled
                callback(url, scaled)
                return
            try:
                os.remove(ruta)
            except OSError:
                pass

        if url in self._descargas_en_curso:
            self._descargas_en_curso[url].append(callback)
            return

        self._descargas_en_curso[url] = [callback]

        worker = _ImageDownloadWorker(url, ruta, target_size)
        # Mantener vivo el wrapper Python hasta recibir la señal de finalización.
        self._workers[url] = worker
        worker.signals.completado.connect(self._al_terminar_descarga)
        self._pool.start(worker)

    def _al_terminar_descarga(self, url: str, img: QImage):
        self._workers.pop(url, None)
        callbacks = self._descargas_en_curso.pop(url, [])
        pixmap = None

        if not img.isNull():
            pixmap = QPixmap.fromImage(img)
            self._ram_cache[url] = pixmap

        for cb in callbacks:
            try:
                cb(url, pixmap)
            except Exception:
                pass

def limpiar_cache_antigua(dias=30):
    import time, os
    from .paths import CACHE_DIR
    if not os.path.exists(CACHE_DIR): return
    ahora = time.time()
    for f in os.listdir(CACHE_DIR):
        ruta = os.path.join(CACHE_DIR, f)
        if os.path.isfile(ruta) and os.stat(ruta).st_mtime < ahora - (dias * 86400):
            try: os.remove(ruta)
            except: pass
