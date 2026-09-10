"""Utilidades y compatibilidad de la ventana principal."""

import hashlib
import os
import webbrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication
from config import (
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_TEXT_PRIMARY,
    COLOR_ACCENT, COLOR_ACCENT_LIGHT,
)


def _centrar(self):
    screen = QApplication.primaryScreen()
    if screen:
        geo = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(geo.center())
        self.move(frame.topLeft())



def _load_store_icon(self, path, logical_size=64):
    """Carga un icono de tienda a resolución física suficiente para el DPI de Qt."""
    if not os.path.exists(path):
        return None

    pixmap = QPixmap(path)
    if pixmap.isNull():
        return None

    screen = QApplication.primaryScreen()
    dpr = screen.devicePixelRatio() if screen is not None else 1.0
    dpr = max(1.0, float(dpr))
    physical_size = max(1, round(logical_size * dpr))

    scaled = pixmap.scaled(
        physical_size, physical_size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    scaled.setDevicePixelRatio(dpr)
    return scaled



def _load_thumbnail(self, url_img):
    if not url_img:
        return None

    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    filename = os.path.join(
        cache_dir,
        f"{hashlib.sha256(url_img.encode('utf-8')).hexdigest()}.png",
    )

    try:
        if os.path.exists(filename):
            pixmap = QPixmap(filename)
            if not pixmap.isNull():
                return pixmap

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        res = requests.get(url_img, headers=headers, timeout=5)
        if res.status_code == 200:
            pixmap = QPixmap()
            if pixmap.loadFromData(res.content):
                pixmap.save(filename, "PNG")
                return pixmap
    except Exception as e:
        print(f"Error descargando miniatura ({url_img}): {e}")
    return None



def _resize_canvas_content(self, event):
    # Compatibilidad nominal con el nombre antiguo.
    if self.frame_lista is not None:
        self.frame_lista.setMinimumWidth(max(1, event.size().width()))



def _mousewheel(self, event):
    # Compatibilidad nominal con el nombre antiguo.
    return None



def abrir_enlace(self, url):
    if url:
        webbrowser.open(url)



def _apply_theme(self, bg, card, desc, text, secondary, icon_path):
    # Compatibilidad con llamadas antiguas: el tema real se obtiene
    # exclusivamente de config.THEMES.
    self.alternar_tema()



def _icons_root(self):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets",
        "icons",
    )



def _icon_path(self, filename):
    return os.path.join(self._icons_root(), "navigation_ui", filename)



def _action_icon_path(self, filename):
    return os.path.join(self._icons_root(), "actions", filename)



def _store_icon_path(self, filename):
    return os.path.join(self._icons_root(), "stores", filename)



def _cerrar_ventana(self):
    self.close()



def closeEvent(self, event):
    try:
        self._detener_audio()
        limpiar_cache_imagenes()
    except Exception:
        pass
    if callable(self.al_cerrar_app):
        try:
            self.al_cerrar_app()
        except Exception:
            pass
    event.accept()



def mostrar(self):
    self.show()
    self.raise_()
    self.activateWindow()
    self._centrar()



def run(self):
    """Compatibilidad con main.py antiguo; QApplication debe existir fuera."""
    self.show()
    self.raise_()
    self.activateWindow()



def instalar_metodos(cls):

    cls._centrar = _centrar

    cls._load_store_icon = _load_store_icon

    cls._load_thumbnail = _load_thumbnail

    cls._resize_canvas_content = _resize_canvas_content

    cls._mousewheel = _mousewheel

    cls.abrir_enlace = abrir_enlace

    cls._apply_theme = _apply_theme

    cls._icons_root = _icons_root

    cls._icon_path = _icon_path

    cls._action_icon_path = _action_icon_path

    cls._store_icon_path = _store_icon_path

    cls._cerrar_ventana = _cerrar_ventana

    cls.closeEvent = closeEvent

    cls.mostrar = mostrar

    cls.run = run
