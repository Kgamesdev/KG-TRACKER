"""Modal de apoyo a Ko-fi para K GAME TRACKER con diseno premium y mensaje personal."""

import os
import webbrowser

from PySide6.QtCore import QEvent, Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
    QGraphicsOpacityEffect, QFrame
)

import config
from config import ICON_PATH
from core.i18n import obtener_idioma
from ui.design_system import FONT_FAMILY, FONT_SIZE_BODY_PT


class KofiModal(QDialog):
    """Modal Qt para apoyar el proyecto mediante Ko-fi con diseno calido y personal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("KG Tracker — Ko-fi")
        self.setFixedSize(500, 320)
        self._outside_click_filter_installed = False

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setModal(False)
        self.setWindowModality(Qt.WindowModality.NonModal)

        idioma = obtener_idioma()
        es_ingles = idioma.startswith("en")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 22)
        layout.setSpacing(14)

        # Encabezado
        titulo_texto = "☕ Thank you for using KG Tracker!" if es_ingles else "☕ ¡Gracias por usar KG Tracker!"
        title = QLabel(titulo_texto)
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setObjectName("separator")
        layout.addWidget(self.separator)

        # Tarjeta con tu mensaje exacto
        card_frame = QFrame()
        card_frame.setObjectName("messageCard")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(18, 14, 18, 14)
        card_layout.setSpacing(10)

        if es_ingles:
            p1_text = (
                "Hi, I'm <b>Kuri</b>. I created KG Tracker in my spare time, "
                "with the hope that nobody misses out on any free games."
            )
            p2_text = (
                "If you enjoy the app and would like to support the project, "
                "buying me a coffee on Ko-fi goes a long way to keep the motivation high "
                "and help cover ongoing development."
            )
            btn_kofi_text = "☕ Buy me a coffee on Ko-fi"
            btn_cancel_text = "Maybe later"
        else:
            p1_text = (
                "Hola, soy <b>Kuri</b>. Creé KG Tracker en mis ratos libres, "
                "con la ilusión de que nadie se pierda ningún juego gratis."
            )
            p2_text = (
                "Si la app te gusta y quieres ayudarme con el proyecto, "
                "invitarme a un café en Ko-fi ayuda un montón a mantener las ganas "
                "y costear el desarrollo continuo."
            )
            btn_kofi_text = "☕ Invitarme a un café en Ko-fi"
            btn_cancel_text = "Quizás luego"

        p1 = QLabel(p1_text)
        p1.setWordWrap(True)
        p1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        card_layout.addWidget(p1)

        p2 = QLabel(p2_text)
        p2.setWordWrap(True)
        p2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        card_layout.addWidget(p2)

        layout.addWidget(card_frame)

        # Botones de accion
        buttons = QHBoxLayout()
        buttons.setSpacing(14)
        buttons.addStretch()

        go = QPushButton(btn_kofi_text)
        go.setObjectName("accentButton")
        go.setCursor(Qt.CursorShape.PointingHandCursor)
        go.clicked.connect(self.ir_a_kofi)
        buttons.addWidget(go)

        cancel = QPushButton(btn_cancel_text)
        cancel.setObjectName("cancelButton")
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.close)
        buttons.addWidget(cancel)

        buttons.addStretch()
        layout.addLayout(buttons)

        self._aplicar_estilos_modal()

        self._inicializar_fade_in_suave()

    def _aplicar_estilos_modal(self):
        """Usa la misma paleta, tipografía y controles que Ajustes."""
        paleta = config.THEMES[config.CURRENT_THEME]
        bg = paleta["COLOR_BG"]
        panel = paleta["COLOR_BG_CARD"]
        field = paleta["COLOR_BG_DESC"]
        text = paleta["COLOR_TEXT_PRIMARY"]
        secondary = paleta["COLOR_TEXT_SECONDARY"]
        border = paleta["COLOR_BORDER"]
        accent = paleta["COLOR_ACCENT"]
        hover = paleta["COLOR_ACCENT_HOVER"]

        self.setStyleSheet(f"""
            QDialog {{ background: {bg}; color: {text}; font-family: '{FONT_FAMILY}'; font-size: {FONT_SIZE_BODY_PT}pt; }}
            QLabel {{ color: {text}; font: {FONT_SIZE_BODY_PT}pt '{FONT_FAMILY}'; }}
            #dialogTitle {{ font: bold 14pt '{FONT_FAMILY}'; }}
            #separator {{ color: {border}; background: {border}; max-height: 1px; }}
            #messageCard {{ background: {panel}; border: 1px solid {border}; border-radius: 9px; }}
            #messageCard QLabel {{ color: {secondary}; font: {FONT_SIZE_BODY_PT}pt '{FONT_FAMILY}'; }}
            #accentButton {{ background: {accent}; color: #FFFFFF; border: 1px solid {accent}; font: bold {FONT_SIZE_BODY_PT}pt '{FONT_FAMILY}'; padding: 9px 18px; border-radius: 8px; }}
            #accentButton:hover {{ background: {hover}; border-color: {hover}; }}
            #accentButton:pressed {{ background: {'#555BB5' if config.CURRENT_THEME == 'light' else '#4338CA'}; }}
            #cancelButton {{ background: {field}; color: {text}; border: 1px solid {border}; font: {FONT_SIZE_BODY_PT}pt '{FONT_FAMILY}'; padding: 9px 18px; border-radius: 8px; }}
            #cancelButton:hover {{ background: {paleta['COLOR_HOVER']}; border-color: {accent}; }}
        """)

    def showEvent(self, event):
        super().showEvent(event)
        app = QApplication.instance()
        if app and not self._outside_click_filter_installed:
            app.installEventFilter(self)
            self._outside_click_filter_installed = True

    def hideEvent(self, event):
        app = QApplication.instance()
        if app and self._outside_click_filter_installed:
            app.removeEventFilter(self)
            self._outside_click_filter_installed = False
        super().hideEvent(event)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.ApplicationDeactivate and self.isVisible():
            self._cerrar_y_volver_a_principal()
            return False
        if event.type() == QEvent.Type.MouseButtonPress and self.isVisible():
            if not self.frameGeometry().contains(event.globalPosition().toPoint()):
                self._cerrar_y_volver_a_principal()
        return super().eventFilter(watched, event)

    def _cerrar_y_volver_a_principal(self):
        if not self.isVisible():
            return
        self.close()
        parent = self.parentWidget()
        if parent is not None:
            QTimer.singleShot(0, parent.showNormal)
            QTimer.singleShot(0, parent.raise_)
            QTimer.singleShot(0, parent.activateWindow)

    def _inicializar_fade_in_suave(self):
        self._efecto_opacidad = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._efecto_opacidad)
        
        self._anim_fade = QPropertyAnimation(self._efecto_opacidad, b"opacity")
        self._anim_fade.setDuration(280)
        self._anim_fade.setStartValue(0.0)
        self._anim_fade.setEndValue(1.0)
        self._anim_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_fade.start()

    def ir_a_kofi(self):
        webbrowser.open_new_tab("https://ko-fi.com/kurigamedeveloper")
        self.close()

