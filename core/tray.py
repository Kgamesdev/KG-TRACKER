import os
import json
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QAction
from PySide6.QtCore import Qt, QTimer
from config import ICON_PATH, BASE_DIR

CONFIG_TRAY_PATH = os.path.join(BASE_DIR, "data", "settings.json")


def _obtener_icono_seguro():
    if os.path.exists(ICON_PATH):
        icono = QIcon(ICON_PATH)
        if not icono.isNull():
            return icono

    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor("#6366F1"))
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


class GameTrackerTray:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.tray_icon = None
        self.icono_app = _obtener_icono_seguro()
        self.timer_busqueda = QTimer(ventana_principal)
        self.timer_busqueda.timeout.connect(self._ejecutar_barrido_segundo_plano)
        self._inicializar()
        self.actualizar_temporizador_busqueda()

    def _inicializar(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self.icono_app, self.ventana)
        self.tray_icon.setToolTip("K Game Tracker — Ofertas activas")

        # Conectar el clic en la propia notificación de Windows para abrir la app
        self.tray_icon.messageClicked.connect(self.mostrar_ventana)

        menu = QMenu()
        accion_abrir = QAction("Mostrar K Game Tracker", self.ventana)
        accion_abrir.triggered.connect(self.mostrar_ventana)
        menu.addAction(accion_abrir)

        accion_buscar = QAction("Comprobar ofertas ahora", self.ventana)
        accion_buscar.triggered.connect(self.ejecutar_barrido_manual)
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
            print(f"⏰ [TRAY] Temporizador configurado a: {frecuencia}")

    def contar_ofertas_disponibles(self):
        try:
            juegos = getattr(self.ventana, "juegos_cache_global", []) or []
            if hasattr(self.ventana, "es_reclamado"):
                disponibles = [j for j in juegos if not self.ventana.es_reclamado(j)]
                return len(disponibles)
            return len(juegos)
        except Exception:
            return 0

    def notificar_al_minimizar(self):
        cfg = _obtener_config()
        if not cfg.get("notificaciones_activas", True):
            return

        cant = self.contar_ofertas_disponibles()
        mensaje = f"Tienes {cant} ofertas disponibles en este momento." if cant > 0 else "Vigilando ofertas en segundo plano."

        if self.tray_icon and self.tray_icon.isVisible():
            # Pasamos self.icono_app en lugar de un icono generico del sistema
            self.tray_icon.showMessage(
                "K Game Tracker minimizado",
                f"{mensaje} Haz clic aquí para volver a abrir.",
                self.icono_app,
                4000
            )

    def ejecutar_barrido_manual(self):
        print("🔍 [TRAY] Barrido manual solicitado por el usuario...")
        self._lanzar_busqueda(manual=True)

    def _ejecutar_barrido_segundo_plano(self):
        print("⏰ [TRAY] Ejecutando barrido automático programado...")
        self._lanzar_busqueda(manual=False)

    def _lanzar_busqueda(self, manual=False):
        try:
            if hasattr(self.ventana, "cargar_juegos_thread"):
                self.ventana.cargar_juegos_thread()
            elif hasattr(self.ventana, "actualizar_ofertas"):
                self.ventana.actualizar_ofertas()

            QTimer.singleShot(2500, lambda: self._reportar_resultado_barrido(manual))
        except Exception as e:
            print(f"⚠️ [TRAY] Error lanzando barrido: {e}")

    def _reportar_resultado_barrido(self, manual=False):
        cfg = _obtener_config()
        if not cfg.get("notificaciones_activas", True):
            return

        cant = self.contar_ofertas_disponibles()
        titulo = "Barrido de ofertas completado" if manual else "Actualización de ofertas"
        cuerpo = f"Se encontraron {cant} ofertas disponibles listas para reclamar." if cant > 0 else "No hay ofertas nuevas por el momento."

        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                titulo,
                cuerpo,
                self.icono_app,
                4500
            )

    def salir_definitivo(self):
        if self.tray_icon:
            self.tray_icon.hide()
        self.ventana._salida_forzada = True
        app = QApplication.instance()
        if app:
            app.quit()
