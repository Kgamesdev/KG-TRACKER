"""Modal de ajustes para K GAME TRACKER basada en PySide6/Qt."""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from config import ICON_PATH


class SettingsModal(QDialog):
    """Modal Qt para los ajustes de la aplicación."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajustes")
        self.setFixedSize(520, 420)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(10)

        title = QLabel("AJUSTES")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("separator")
        layout.addWidget(line)

        options = QVBoxLayout()
        options.setSpacing(12)
        layout.addLayout(options)

        def add_row(text, values):
            row = QHBoxLayout()
            label = QLabel(text)
            combo = QComboBox()
            combo.addItems(values)
            combo.setMinimumWidth(180)
            row.addWidget(label)
            row.addStretch()
            row.addWidget(combo)
            options.addLayout(row)

        add_row("Idioma de la interfaz", ["Español (ES)", "English (EN)"])
        add_row("Tema visual", ["Neón Cyberpunk", "Oscuro Clásico", "Minimalista"])
        add_row("Buscar ofertas automáticamente", ["Al iniciar", "Cada hora", "Desactivado"])

        row = QHBoxLayout()
        row.addWidget(QLabel("Iniciar minimizado con Windows"))
        row.addStretch()
        self.chk_var = QCheckBox()
        row.addWidget(self.chk_var)
        options.addLayout(row)
        options.addStretch()

        save = QPushButton("GUARDAR CAMBIOS")
        save.setObjectName("accentButton")
        save.clicked.connect(self.close)
        layout.addWidget(save)

        self.setStyleSheet(
            "QDialog { background: #1E1E2E; color: #FFFFFF; }"
            "QLabel { color: #FFFFFF; font: 11pt 'Segoe UI'; }"
            "#dialogTitle { font: bold 14pt 'Segoe UI'; }"
            "#separator { color: #2A2A3A; background: #2A2A3A; max-height: 1px; }"
            "QComboBox { background: #2A2A3A; color: #FFFFFF; border: 0; padding: 5px; }"
            "QCheckBox { color: #FFFFFF; }"
            "#accentButton { background: #5865F2; color: #FFFFFF; font: bold 10pt 'Segoe UI'; padding: 9px; }"
            "#accentButton:hover { background: #4752C4; }"
        )
