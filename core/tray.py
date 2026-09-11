import os
import json
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QAction
from PySide6.QtCore import Qt
from config import ICON_PATH, BASE_DIR

CONFIG_TRAY_PATH = os.path.join(BASE_DIR, "data", "settings.json")


def _obtener_icono_seguro():
    """Obtiene un QIcon garantizado para que Windows nunca lo ignore."""
    if os.path.exists(ICON_PATH):
        icono = QIcon(ICON_PATH)
        if not icono.isNull():
            return icono

    # Si por alguna razón el archivo .ico no está o falla, generamos uno nítido en memoria
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor("#6366F1"))  # Color morado/azul de la app
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(2, 2, 28, 28, 6, 6)
    painter.end()
    return QIcon(pixmap)


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
            print("⚠️ [TRAY] El sistema operativo no tiene soporte para bandeja.")
            return

        icono = _obtener_icono_seguro()
        
        # Anclar firmemente al objeto de la ventana para evitar Garbage Collection
        self.tray_icon = QSystemTrayIcon(icono, self.ventana)
        self.tray_icon.setToolTip("K Game Tracker — Ofertas Activas")

        # Menú contextual
        menu = QMenu()

        accion_abrir = QAction("Mostrar K Game Tracker", self.ventana)
        accion_abrir.triggered.connect(self.mostrar_ventana)
        menu.addAction(accion_abrir)

        menu.addSeparator()

        accion_salir = QAction("Salir completamente", self.ventana)
        accion_salir.triggered.connect(self.salir_definitivo)
        menu.addAction(accion_salir)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._on_activado)
        
        # Mostrar el icono en Windows
        self.tray_icon.show()
        self.tray_icon.setVisible(True)
        print("✅ [TRAY] Icono registrado y visible en la barra de Windows.")

    def _on_activado(self, reason):
        # Click normal (Trigger) o Doble Click abre la app
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self.mostrar_ventana()

    def mostrar_ventana(self):
        self.ventana.showNormal()
        self.ventana.raise_()
        self.ventana.activateWindow()
        if hasattr(self.ventana, "reanudar_musica_con_fade"):
            self.ventana.reanudar_musica_con_fade()

    def notificar_primer_cierre(self):
        cfg = _obtener_config()
        if not cfg.get("aviso_bandeja_mostrado", False):
            if self.tray_icon and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    "K Game Tracker sigue activo",
                    "La aplicación se minimizó aquí. Haz clic para abrirla de nuevo.",
                    QSystemTrayIcon.MessageIcon.Information,
                    4000
                )
            cfg["aviso_bandeja_mostrado"] = True
            _guardar_config(cfg)

    def salir_definitivo(self):
        if self.tray_icon:
            self.tray_icon.hide()
        self.ventana._salida_forzada = True
        app = QApplication.instance()
        if app:
            app.quit()
