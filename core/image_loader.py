"""Gestor de descarga y caché asíncrona de miniaturas para KG Tracker."""

import os
import hashlib
import requests
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool, Qt, QSize
from PySide6.QtGui import QImage, QPixmap

from config import BASE_DIR

CACHE_DIR = os.path.join(BASE_DIR, "cache")


class _ImageWorkerSignals(QObject):
    completado = Signal(str, QImage)  # url, imagen descargada y reescalada


class _ImageDownloadWorker(QRunnable):
    """Worker que descarga, cachea y pre-escala la imagen en un hilo secundario."""

    def __init__(self, url: str, ruta_disco: str, target_size: tuple = (190, 104)):
        super().__init__()
        self.url = url
        self.ruta_disco = ruta_disco
        self.target_size = target_size
        self.signals = _ImageWorkerSignals()

    def run(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        try:
            resp = requests.get(self.url, headers=headers, timeout=8)
            if resp.status_code == 200:
                img = QImage()
                if img.loadFromData(resp.content):
                    # Guardar archivo original en caché de disco
                    try:
                        img.save(self.ruta_disco, "PNG")
                    except Exception:
                        pass

                    # Pre-escalar en el hilo secundario para ahorrar CPU en el hilo principal
                    scaled = img.scaled(
                        self.target_size[0],
                        self.target_size[1],
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    self.signals.completado.emit(self.url, scaled)
                    return
        except Exception:
            pass

        # Si falla la descarga, emite una imagen vacía
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
        self._ram_cache = {}          # url -> QPixmap
        self._descargas_en_curso = {}  # url -> lista de callbacks pendientes
        self._pool = QThreadPool.globalInstance()

    def _ruta_cache(self, url: str) -> str:
        hash_url = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return os.path.join(CACHE_DIR, f"{hash_url}.png")

    def cargar(self, url: str, callback, target_size: tuple = (190, 104)):
        """
        Punto de entrada principal:
        1. Devuelve inmediatamente si está en RAM o Disco.
        2. Si no, agenda la descarga en QThreadPool y llama al callback al terminar.
        """
        if not url:
            callback(url, None)
            return

        # 1. Comprobar RAM
        if url in self._ram_cache:
            callback(url, self._ram_cache[url])
            return

        # 2. Comprobar Disco
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

        # 3. Deduplicación de descargas simultáneas
        if url in self._descargas_en_curso:
            self._descargas_en_curso[url].append(callback)
            return

        self._descargas_en_curso[url] = [callback]

        # 4. Lanzar Worker asíncrono
        worker = _ImageDownloadWorker(url, ruta, target_size)
        worker.signals.completado.connect(self._al_terminar_descarga)
        self._pool.start(worker)

    def _al_terminar_descarga(self, url: str, img: QImage):
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
