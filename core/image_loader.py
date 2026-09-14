"""Gestor de descarga y caché asíncrona de miniaturas optimizado para KG Tracker."""

import os
import hashlib
import requests
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool, Qt
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath

from config import BASE_DIR

CACHE_DIR = os.path.join(BASE_DIR, "cache")

def _redondear_qimage(img: QImage, radio: int = 8) -> QImage:
    """Recorta las esquinas nativamente en C++ fuera del hilo principal."""
    if img.isNull(): return img
    img = img.convertToFormat(QImage.Format.Format_ARGB32_Premultiplied)
    out = QImage(img.size(), QImage.Format.Format_ARGB32_Premultiplied)
    out.fill(Qt.GlobalColor.transparent)
    p = QPainter(out)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    path = QPainterPath()
    path.addRoundedRect(0, 0, img.width(), img.height(), radio, radio)
    p.setClipPath(path)
    p.drawImage(0, 0, img)
    p.end()
    return out

class _ImageWorkerSignals(QObject):
    completado = Signal(str, QImage)

class _ImageWorker(QRunnable):
    """Worker que absorbe I/O de disco, red y procesado grafico (escalado/redondeo)."""
    def __init__(self, url, ruta_disco, target_size, session):
        super().__init__()
        self.url = url
        self.ruta_disco = ruta_disco
        self.target_size = target_size
        self.session = session
        self.signals = _ImageWorkerSignals()

    def run(self):
        img = QImage()
        loaded = False
        
        # 1. Intentar cargar desde disco (I/O en background, libera la UI)
        if os.path.exists(self.ruta_disco):
            if img.load(self.ruta_disco):
                loaded = True
        
        # 2. Si no esta en disco, descargar de red
        if not loaded:
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                resp = self.session.get(self.url, headers=headers, timeout=8)
                if resp.status_code == 200:
                    if img.loadFromData(resp.content):
                        loaded = True
                        try:
                            img.save(self.ruta_disco, "PNG")
                        except Exception:
                            pass
            except Exception:
                pass

        if loaded and not img.isNull():
            # Escalar y redondear usando el 100% de la CPU libre del hilo
            scaled = img.scaled(
                self.target_size[0], self.target_size[1],
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            final_img = _redondear_qimage(scaled, 8)
            self.signals.completado.emit(self.url, final_img)
        else:
            self.signals.completado.emit(self.url, QImage())

class ImageLoader(QObject):
    """Singleton coordinador de carga de imagenes de ultra bajo impacto."""
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
        self._pool = QThreadPool.globalInstance()
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=12, pool_maxsize=12)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def _ruta_cache(self, url: str) -> str:
        hash_url = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return os.path.join(CACHE_DIR, f"{hash_url}.png")

    def cargar(self, url: str, callback, target_size: tuple = (190, 104)):
        if not url:
            callback(url, None)
            return

        # 1. Hit en RAM -> Inmediato en UI Thread (Cero coste)
        if url in self._ram_cache:
            callback(url, self._ram_cache[url])
            return

        # 2. Deduplicacion y Despacho a Background
        if url in self._descargas_en_curso:
            self._descargas_en_curso[url].append(callback)
            return

        self._descargas_en_curso[url] = [callback]
        ruta = self._ruta_cache(url)
        
        worker = _ImageWorker(url, ruta, target_size, self._session)
        worker.signals.completado.connect(self._al_terminar_worker)
        self._pool.start(worker)

    def _al_terminar_worker(self, url: str, img: QImage):
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
