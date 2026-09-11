import os
import json
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from config import ICON_PATH, BASE_DIR

CONFIG_TRAY_PATH = os.path.join(BASE_DIR, "data", "settings.json")


def _obtener_config():
    if os.path.exists(CONFIG_TRAY_PATH):
        try:
            with open(CONFIG_TRAY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _guardar_config(datos):
    os.makedirs(os.path.dirname(CONFIG_TRAY_PATH), exist_ok=True)
    try:
        with open(CONFIG_TRAY_PATH, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class GameTrackerTray:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.tray_icon = None
        self._inicializar()

    def _inicializar(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        icono = QIcon(ICON_PATH) if os.path.exists(ICON_PATH) else self.ventana.windowIcon()
        self.tray_icon = QSystemTrayIcon(icono, self.ventana)
        self.tray_icon.setToolTip("K Game Tracker — Buscando juegos gratis")

        # Menú contextual
        menu = QMenu()
        
        accion_abrir = QAction("Abrir K Game Tracker", self.ventana)
        accion_abrir.triggered.connect(self.mostrar_ventana)
        menu.addAction(accion_abrir)

        menu.addSeparator()

        accion_salir = QAction("Salir completamente", self.ventana)
        accion_salir.triggered.connect(self.salir_definitivo)
        menu.addAction(accion_salir)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._on_activado)
        self.tray_icon.show()

    def _on_activado(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self.mostrar_ventana()

    def mostrar_ventana(self):
        self.ventana.show()
        self.ventana.raise_()
        self.ventana.activateWindow()

    def notificar_primer_cierre(self):
        cfg = _obtener_config()
        if not cfg.get("aviso_bandeja_mostrado", False):
            if self.tray_icon:
                self.tray_icon.showMessage(
                    "K Game Tracker sigue activo",
                    "La aplicación se ha minimizado junto al reloj. Haz clic aquí o doble clic en el icono para abrirla.",
                    QSystemTrayIcon.MessageIcon.Information,
                    4000
                )
            cfg["aviso_bandeja_mostrado"] = True
            _guardar_config(cfg)

    def notificar_nuevo_juego(self, titulo, tienda):
        if self.tray_icon:
            self.tray_icon.showMessage(
                "¡Nuevo juego gratis disponible!",
                f"{titulo} está disponible gratis en {tienda}.",
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )

    def salir_definitivo(self):
        self.tray_icon.hide()
        self.ventana._salida_forzada = True
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()
