from core.tray import GameTrackerTray
"""Ventana principal coordinadora de K GAME TRACKER."""

import sys
import os
import config

from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon

from config import WINDOW_TITLE, ICON_PATH, LOGO_PATH, STORES_MAPPING
from core.images import limpiar_cache_imagenes
from ui.kofi_modal import KofiModal
from ui.settings_modal import SettingsModal
from ui.game_card import RoundedButton, VolumeSlider, GameCard
from ui.store_widget import StoreWidget
from ui.main_window_theme import instalar_metodos as instalar_metodos_tema
from ui.main_window_ui import instalar_metodos as instalar_metodos_ui
from ui.main_window_audio import instalar_metodos as instalar_metodos_audio
from ui.main_window_games import instalar_metodos as instalar_metodos_games
from ui.main_window_history import instalar_metodos as instalar_metodos_history
from ui.main_window_navigation import instalar_metodos as instalar_metodos_navigation
from ui.main_window_helpers import instalar_metodos as instalar_metodos_helpers


class VentanaPrincipal(QMainWindow):
    """Ventana principal de K GAME TRACKER con renderizado anti-parpadeo profesional."""

    def __init__(self, parent=None, al_cerrar_app=None, mostrar=True):
        super().__init__(parent if isinstance(parent, QWidget) else None)
        self.parent = parent
        self.al_cerrar_app = al_cerrar_app

        # Alias de compatibilidad con el código existente.
        self.ventana = self

        # 1. Congelar el motor de renderizado antes de que nazca un solo elemento gráfico
        self.setUpdatesEnabled(False)

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(980, 360)
        self.resize(1120, 360)
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.es_modo_oscuro = config.CURRENT_THEME == "dark"
        self.audio_silenciado = False
        self.volumen_anterior = 20
        self.btn_mute = None
        self.todas_activado = False
        self.juegos_cache_global = []
        self.active_filters = {store: False for store in STORES_MAPPING.values()}
        self.acordeon_estados = {}
        self.tienda_seleccionada = None
        self.bubble_widgets = {}
        self._image_refs = []
        self.mostrando_reclamados = False
        self.reclamados = self._cargar_reclamados()

        self._build_ui()
        self._apply_theme_qss()
        self._ajustar_ventana_por_estado(False)
        
        # Preparar la capa interna para un desvanecimiento óptico limpio
        if self.centralWidget():
            self._efecto_entrada = QGraphicsOpacityEffect(self.centralWidget())
            self.centralWidget().setGraphicsEffect(self._efecto_entrada)
            self._efecto_entrada.setOpacity(0.0)

        if mostrar:
            self.show()

    def showEvent(self, event):
        """Intercepta el instante exacto en que la ventana se posiciona en Windows."""
        super().showEvent(event)
        
        # 2. Descongelar los gráficos e iniciar el Fade In fluido solo cuando la geometría es 100% estable
        if not self.updatesEnabled():
            self.setUpdatesEnabled(True)
            QApplication.processEvents() # Forzar sincronización del búfer de vídeo
            
            if self.centralWidget() and hasattr(self, '_efecto_entrada'):
                self._anim_entrada = QPropertyAnimation(self._efecto_entrada, b"opacity")
                self._anim_entrada.setDuration(480) # Duración sedosa cinematográfica
                self._anim_entrada.setStartValue(0.0)
                self._anim_entrada.setEndValue(1.0)
                self._anim_entrada.setEasingCurve(QEasingCurve.Type.OutCubic)
                self._anim_entrada.start()


# Los métodos especializados se instalan en la misma clase para conservar
# exactamente la API y las llamadas self existentes.
instalar_metodos_tema(VentanaPrincipal)
instalar_metodos_ui(VentanaPrincipal)
instalar_metodos_audio(VentanaPrincipal)
instalar_metodos_games(VentanaPrincipal)
instalar_metodos_history(VentanaPrincipal)
instalar_metodos_navigation(VentanaPrincipal)
instalar_metodos_helpers(VentanaPrincipal)


if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())


    def closeEvent(self, event):
        if getattr(self, "_salida_forzada", False):
            event.accept()
            return

        if self._tray is None:
            try:
                self._tray = GameTrackerTray(self)
            except Exception:
                pass

        event.ignore()
        self.hide()
        if self._tray:
            self._tray.notificar_primer_cierre()
