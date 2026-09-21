"""Modal de apoyo a Ko-fi para K GAME TRACKER con diseno premium y mensaje personal."""

import os
import webbrowser

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, 
    QGraphicsOpacityEffect, QFrame
)

from config import ICON_PATH
from core.i18n import obtener_idioma


class KofiModal(QDialog):
    """Modal Qt para apoyar el proyecto mediante Ko-fi con diseno calido y personal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("KG Tracker — Ko-fi")
        self.setFixedSize(500, 320)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setModal(True)

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
        go.setObjectName("kofiButton")
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

        # Estilos visuales pulidos
        self.setStyleSheet("""
            QDialog {
                background: #181926;
                border: 1px solid #2B2D42;
                border-radius: 14px;
            }
            #dialogTitle {
                color: #CAD3F5;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 15pt;
                padding-bottom: 2px;
            }
            #messageCard {
                background: #24273A;
                border: 1px solid #363A4F;
                border-radius: 10px;
            }
            QLabel {
                color: #B8C0E0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10.5pt;
                line-height: 1.45;
            }
            #kofiButton {
                background: #FF5E5B;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 10.5pt;
                border-radius: 8px;
                padding: 9px 20px;
                border: none;
            }
            #kofiButton:hover {
                background: #FF706E;
            }
            #kofiButton:pressed {
                background: #E54B48;
            }
            #cancelButton {
                background: #363A4F;
                color: #CAD3F5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10pt;
                border-radius: 8px;
                padding: 9px 18px;
                border: none;
            }
            #cancelButton:hover {
                background: #494D64;
                color: #FFFFFF;
            }
        """)

        self._inicializar_fade_in_suave()

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

