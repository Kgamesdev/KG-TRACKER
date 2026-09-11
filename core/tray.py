import os
import json
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QAction
from PySide6.QtCore import Qt, QTimer
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
        self.timer_busqueda = QTimer(ventana_principal)
        self.timer_busqueda.timeout.connect(self._ejecutar_barrido_segundo_plano)
        self._inicializar()
        self.actualizar_temporizador_busqueda()

    def _inicializar(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        icono = QIcon(ICON_PATH) if os.path.exists(ICON_PATH) else self.ventana.windowIcon()
        self.tray_icon = QSystemTrayIcon(icono, self.ventana)
        self.tray_icon.setToolTip("K Game Tracker — Ofertas activas")

        menu = QMenu()
        accion_abrir = QAction("Mostrar K Game Tracker", self.ventana)
        accion_abrir.triggered.connect(self.mostrar_ventana)
        menu.addAction(accion_abrir)

        accion_buscar = QAction("Comprobar ofertas ahora", self.ventana)
        accion_buscar.triggered.connect(self._ejecutar_barrido_segundo_plano)
        menu.addAction(accion_buscar)

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
        self.ventana.showNormal()
        self.ventana.raise_()
        self.ventana.activateWindow()
        if hasattr(self.ventana, "reanudar_musica_con_fade"):
            self.ventana.reanudar_musica_con_fade()

    def actualizar_temporizador_busqueda(self):
        cfg = _obtener_config()
        frecuencia = cfg.get("frecuencia_busqueda", "Cada 4 horas")
        self.timer_busqueda.stop()

        horas_map = {
            "Cada 2 horas": 2,
            "Cada 4 horas": 4,
            "Cada 8 horas": 8,
            "Una vez al día (24h)": 24
        }

        if frecuencia in horas_map:
            ms = horas_map[frecuencia] * 3600 * 1000
            self.timer_busqueda.setInterval(ms)
            self.timer_busqueda.start()
            print(f"⏰ [TRAY] Temporizador de ofertas configurado a: {frecuencia}")
        else:
            print("⏰ [TRAY] Temporizador en segundo plano desactivado.")

    def _ejecutar_barrido_segundo_plano(self):
        """Consulta la API en segundo plano y avisa si hay nuevas ofertas no reclamadas."""
        cfg = _obtener_config()
        if not cfg.get("notificaciones_activas", True):
            return

        print("🔍 [TRAY] Ejecutando barrido automático de ofertas...")
        try:
            # Invocar la búsqueda existente de la app sin bloquear
            if hasattr(self.ventana, "cargar_juegos_thread"):
                self.ventana.cargar_juegos_thread(silencioso=True)
            elif hasattr(self.ventana, "actualizar_ofertas"):
                self.ventana.actualizar_ofertas()
        except Exception as e:
            print(f"⚠️ [TRAY] Error en barrido: {e}")

    def notificar_primer_cierre(self):
        cfg = _obtener_config()
        if not cfg.get("aviso_bandeja_mostrado", False):
            if self.tray_icon and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    "K Game Tracker sigue vigilando",
                    "Seguimos rastreando ofertas en segundo plano según tu frecuencia elegida.",
                    QSystemTrayIcon.MessageIcon.NoIcon,
                    4500
                )
            cfg["aviso_bandeja_mostrado"] = True
            _guardar_config(cfg)

    def notificar_nuevos_juegos(self, cantidad):
        cfg = _obtener_config()
        if not cfg.get("notificaciones_activas", True):
            return

        if self.tray_icon and self.tray_icon.isVisible() and cantidad > 0:
            self.tray_icon.showMessage(
                "¡Nuevos juegos gratis detectados!",
                f"Hay {cantidad} ofertas nuevas listas para reclamar.",
                QSystemTrayIcon.MessageIcon.NoIcon,
                5000
            )

    def salir_definitivo(self):
        if self.tray_icon:
            self.tray_icon.hide()
        self.ventana._salida_forzada = True
        app = QApplication.instance()
        if app:
            app.quit()
