"""Modal de apoyo a Ko-fi para K GAME TRACKER basada en PySide6/Qt."""

import os
import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from config import ICON_PATH


class KofiModal(QDialog):
    """Modal Qt para apoyar el proyecto mediante Ko-fi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Apoyar K Game Tracker")
        self.setFixedSize(460, 280)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        title = QLabel("☕ ¿Apoyar el proyecto?")
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        desc = QLabel(
            "K Game Tracker es gratuito y se mantiene con esfuerzo.\n"
            "¡Invítame a un café! :)"
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        buttons = QHBoxLayout()
        buttons.addStretch()

        go = QPushButton("Continuar a Ko-fi")
        go.setObjectName("accentButton")
        go.clicked.connect(self.ir_a_kofi)
        buttons.addWidget(go)

        cancel = QPushButton("Cancelar")
        cancel.clicked.connect(self.close)
        buttons.addWidget(cancel)

        buttons.addStretch()
        layout.addLayout(buttons)

        self.setStyleSheet(
            "QDialog { background: #1E1E2E; color: #FFFFFF; }"
            "QLabel { color: #B0B0C0; font: 10pt 'Segoe UI'; }"
            "#dialogTitle { color: #FFFFFF; font: bold 14pt 'Segoe UI'; }"
            "QPushButton { background: #2A2A3A; color: #FFFFFF; border: 0; padding: 8px 15px; }"
            "#accentButton { background: #FFDD00; color: #000000; font: bold 10pt 'Segoe UI'; }"
            "#accentButton:hover { background: #E6C800; }"
        )

    def ir_a_kofi(self):
        webbrowser.open_new_tab("https://ko-fi.com/kurigamedeveloper")
        self.close()
