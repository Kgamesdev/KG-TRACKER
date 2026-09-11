"""Modal de ajustes para K GAME TRACKER basada en PySide6/Qt."""
import os
import json

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

from config import ICON_PATH, BASE_DIR
from core.autostart import habilitar_autostart, deshabilitar_autostart, autostart_activo

SETTINGS_FILE = os.path.join(BASE_DIR, "data", "settings.json")


def cargar_ajustes():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def guardar_ajustes(data):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class SettingsModal(QDialog):
    """Modal Qt para los ajustes de la aplicación con lógica real de persistencia."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajustes")
        self.setFixedSize(520, 430)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setModal(True)
        self.config_actual = cargar_ajustes()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        title = QLabel("AJUSTES")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("separator")
        layout.addWidget(line)

        options = QVBoxLayout()
        options.setSpacing(10)

        # Diccionario para guardar referencias de los combos
        self.combos = {}

        def add_row(key, label_text, values, default_val):
            row = QHBoxLayout()
            label = QLabel(label_text)
            combo = QComboBox()
            combo.addItems(values)
            combo.setMinimumWidth(190)

            # Seleccionar el valor actual guardado
            valor_guardado = self.config_actual.get(key, default_val)
            idx = combo.findText(valor_guardado)
            if idx >= 0:
                combo.setCurrentIndex(idx)

            row.addWidget(label)
            row.addStretch()
            row.addWidget(combo)
            options.addLayout(row)
            self.combos[key] = combo

        # Filas de configuración
        add_row(
            "frecuencia_busqueda",
            "Buscar ofertas automáticamente",
            ["Cada 2 horas", "Cada 4 horas", "Cada 8 horas", "Una vez al día (24h)", "Solo al iniciar", "Desactivado"],
            "Cada 4 horas"
        )

        add_row(
            "idioma",
            "Idioma de la interfaz",
            ["Español (ES)", "English (EN)"],
            "Español (ES)"
        )

        add_row(
            "tema",
            "Tema visual",
            ["Neón Cyberpunk (Oscuro)", "Minimalista Claro"],
            "Neón Cyberpunk (Oscuro)"
        )

        # Checkbox Iniciar con Windows (Autostart voluntario)
        row_auto = QHBoxLayout()
        row_auto.addWidget(QLabel("Iniciar con Windows (minimizado)"))
        row_auto.addStretch()
        self.chk_autostart = QCheckBox()
        self.chk_autostart.setChecked(autostart_activo())
        row_auto.addWidget(self.chk_autostart)
        options.addLayout(row_auto)

        # Checkbox Notificaciones de escritorio
        row_notif = QHBoxLayout()
        row_notif.addWidget(QLabel("Mostrar notificaciones de ofertas"))
        row_notif.addStretch()
        self.chk_notif = QCheckBox()
        self.chk_notif.setChecked(self.config_actual.get("notificaciones_activas", True))
        row_notif.addWidget(self.chk_notif)
        options.addLayout(row_notif)

        layout.addLayout(options)
        layout.addStretch()

        save = QPushButton("GUARDAR CAMBIOS")
        save.setObjectName("accentButton")
        save.clicked.connect(self._guardar_y_cerrar)
        layout.addWidget(save)

        self.setStyleSheet(
            "QDialog { background: #1E1E2E; color: #FFFFFF; }"
            "QLabel { color: #FFFFFF; font: 10pt 'Segoe UI'; }"
            "#dialogTitle { font: bold 14pt 'Segoe UI'; }"
            "#separator { color: #2A2A3A; background: #2A2A3A; max-height: 1px; }"
            "QComboBox { background: #2A2A3A; color: #FFFFFF; border: 1px solid #3A3A50; padding: 5px; border-radius: 4px; }"
            "QComboBox QAbstractItemView { background: #1E1E2E; color: #FFFFFF; selection-background-color: #6366F1; }"
            "QCheckBox { color: #FFFFFF; }"
            "#accentButton { background: #6366F1; color: #FFFFFF; font: bold 10pt 'Segoe UI'; padding: 10px; border-radius: 6px; }"
            "#accentButton:hover { background: #4F46E5; }"
        )

    def _guardar_y_cerrar(self):
        # 1. Guardar preferencias en JSON
        self.config_actual["frecuencia_busqueda"] = self.combos["frecuencia_busqueda"].currentText()
        self.config_actual["idioma"] = self.combos["idioma"].currentText()
        self.config_actual["tema"] = self.combos["tema"].currentText()
        self.config_actual["notificaciones_activas"] = self.chk_notif.isChecked()
        guardar_ajustes(self.config_actual)

        # 2. Gestionar inicio con Windows
        if self.chk_autostart.isChecked():
            habilitar_autostart()
        else:
            deshabilitar_autostart()

        # 3. Notificar a la ventana principal / Tray si existen para actualizar temporizador
        parent = self.parent()
        if parent and hasattr(parent, "_tray") and parent._tray:
            parent._tray.actualizar_temporizador_busqueda()

        self.accept()
