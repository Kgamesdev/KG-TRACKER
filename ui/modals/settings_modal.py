"""Modal de ajustes para K GAME TRACKER basada en PySide6/Qt."""
import os
import json

from PySide6.QtCore import Qt, QSize
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

import config
from config import ICON_PATH, BASE_DIR
from core.autostart import habilitar_autostart, deshabilitar_autostart, autostart_activo
from core.i18n import t, establecer_idioma, obtener_idioma, IDIOMAS, MAPEO_FRECUENCIA, MAPEO_TEMAS

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("settings.title"))
        self.setFixedSize(520, 430)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setModal(True)
        self.config_actual = cargar_ajustes()
        self.tema_original = config.CURRENT_THEME
        self.idioma_activo = obtener_idioma()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        self.title = QLabel(t("settings.title"))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("dialogTitle")
        layout.addWidget(self.title)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setObjectName("separator")
        layout.addWidget(self.line)

        options = QVBoxLayout()
        options.setSpacing(10)
        self.combos = {}

        def add_row(key, label_text, values, default_idx=0):
            row = QHBoxLayout()
            label = QLabel(label_text)
            combo = QComboBox()
            combo.addItems(values)
            combo.setMinimumWidth(190)

            # Buscar índice si había algo guardado
            valor_guardado = self.config_actual.get(key, "")
            idx = combo.findText(valor_guardado)
            if idx >= 0:
                combo.setCurrentIndex(idx)
            else:
                combo.setCurrentIndex(default_idx)

            row.addWidget(label)
            row.addStretch()
            row.addWidget(combo)
            options.addLayout(row)
            self.combos[key] = combo

        # 1. Frecuencia bilingüe
        lista_freq = MAPEO_FRECUENCIA.get(self.idioma_activo, MAPEO_FRECUENCIA["es"])
        add_row("frecuencia_busqueda", t("settings.freq_label"), lista_freq, 1)

        # 2. Idioma
        lista_idiomas = list(IDIOMAS.values())
        idx_lang = 1 if self.idioma_activo == "en" else 0
        add_row("idioma", t("settings.lang_label"), lista_idiomas, idx_lang)

        # 3. Tema bilingüe
        lista_temas = MAPEO_TEMAS.get(self.idioma_activo, MAPEO_TEMAS["es"])
        idx_tema = 1 if config.CURRENT_THEME == "light" else 0
        add_row("tema", t("settings.theme_label"), lista_temas, idx_tema)
        self.combos["tema"].currentTextChanged.connect(self._al_cambiar_tema_en_vivo)

        # 4. Iniciar con Windows
        row_auto = QHBoxLayout()
        row_auto.addWidget(QLabel(t("settings.autostart_label")))
        row_auto.addStretch()
        self.chk_autostart = QCheckBox()
        self.chk_autostart.setChecked(autostart_activo())
        row_auto.addWidget(self.chk_autostart)
        options.addLayout(row_auto)

        # 5. Notificaciones de escritorio
        row_notif = QHBoxLayout()
        row_notif.addWidget(QLabel(t("settings.notif_label")))
        row_notif.addStretch()
        self.chk_notif = QCheckBox()
        self.chk_notif.setChecked(self.config_actual.get("notificaciones_activas", True))
        row_notif.addWidget(self.chk_notif)
        options.addLayout(row_notif)

        layout.addLayout(options)
        layout.addStretch()

        self.btn_save = QPushButton(t("settings.save_btn"))
        self.btn_save.setObjectName("accentButton")
        self.btn_save.clicked.connect(self._guardar_y_cerrar)
        layout.addWidget(self.btn_save)

        self._aplicar_estilos_modal()

    def _aplicar_estilos_modal(self):
        es_claro = (config.CURRENT_THEME == "light")
        bg_dialog = "#D8E4F3" if es_claro else "#1E1E2E"
        texto_color = "#0F1E33" if es_claro else "#FFFFFF"
        combo_bg = "#C4D5EA" if es_claro else "#2A2A3A"
        borde_color = "#8EA7C7" if es_claro else "#3A3A50"
        separador = "#8EA7C7" if es_claro else "#2A2A3A"
        btn_bg = "#4356D6" if es_claro else "#6366F1"
        btn_hover = "#3545B3" if es_claro else "#4F46E5"

        self.setStyleSheet(f"""
            QDialog {{ background: {bg_dialog}; color: {texto_color}; }}
            QLabel {{ color: {texto_color}; font: 10pt 'Segoe UI'; }}
            #dialogTitle {{ font: bold 14pt 'Segoe UI'; }}
            #separator {{ color: {separador}; background: {separador}; max-height: 1px; }}
            QComboBox {{ background: {combo_bg}; color: {texto_color}; border: 1px solid {borde_color}; padding: 5px; border-radius: 4px; }}
            QComboBox QAbstractItemView {{ background: {bg_dialog}; color: {texto_color}; selection-background-color: {btn_bg}; }}
            QCheckBox {{ color: {texto_color}; }}
            #accentButton {{ background: {btn_bg}; color: #FFFFFF; font: bold 10pt 'Segoe UI'; padding: 10px; border-radius: 6px; }}
            #accentButton:hover {{ background: {btn_hover}; }}
        """)

    def _sincronizar_tema_nativo(self, tema_clave):
        parent = self.parent()
        if not parent:
            return

        config.CURRENT_THEME = tema_clave
        parent.es_modo_oscuro = (tema_clave == "dark")

        if hasattr(parent, "_apply_theme_qss"):
            parent._apply_theme_qss()
        if hasattr(parent, "btn_side_theme") and hasattr(parent, "_icon_path"):
            icon_file = "light_theme.png" if parent.es_modo_oscuro else "dark_theme.png"
            path = parent._icon_path(icon_file)
            parent.btn_side_theme.setIcon(QIcon(path))
            parent.btn_side_theme.setIconSize(QSize(28, 28))
        if hasattr(parent, "_actualizar_estilo_botones"):
            parent._actualizar_estilo_botones()
        if hasattr(parent, "_sync_theme_properties"):
            parent._sync_theme_properties()

    def _al_cambiar_tema_en_vivo(self, texto_tema):
        t_low = texto_tema.lower()
        tema_clave = "light" if ("claro" in t_low or "light" in t_low) else "dark"
        if config.CURRENT_THEME == tema_clave:
            return
        self._sincronizar_tema_nativo(tema_clave)
        self._aplicar_estilos_modal()

    def _guardar_y_cerrar(self):
        tema_elegido_txt = self.combos["tema"].currentText()
        t_low = tema_elegido_txt.lower()
        tema_clave = "light" if ("claro" in t_low or "light" in t_low) else "dark"

        idioma_seleccionado_txt = self.combos["idioma"].currentText()
        lang_code = "en" if "English" in idioma_seleccionado_txt else "es"
        establecer_idioma(lang_code)

        self.config_actual["frecuencia_busqueda"] = self.combos["frecuencia_busqueda"].currentText()
        self.config_actual["idioma"] = idioma_seleccionado_txt
        self.config_actual["idioma_codigo"] = lang_code
        self.config_actual["tema"] = tema_elegido_txt
        self.config_actual["tema_clave"] = tema_clave
        self.config_actual["notificaciones_activas"] = self.chk_notif.isChecked()
        guardar_ajustes(self.config_actual)

        if self.chk_autostart.isChecked():
            habilitar_autostart()
        else:
            deshabilitar_autostart()

        parent = self.parent()
        if parent:
            if hasattr(parent, "_actualizar_textos_idioma"):
                parent._actualizar_textos_idioma()
            if hasattr(parent, "_tray") and parent._tray:
                parent._tray.actualizar_temporizador_busqueda()

        self.accept()

    def reject(self):
        if config.CURRENT_THEME != self.tema_original:
            self._sincronizar_tema_nativo(self.tema_original)
        super().reject()
