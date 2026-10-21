"""Modal de ajustes para K GAME TRACKER basada en PySide6/Qt."""
import os
import json

from PySide6.QtCore import QEvent, Qt, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QGroupBox,
    QVBoxLayout,
)

import config
from config import ICON_PATH, BASE_DIR
from core.storage import guardar_json_atomico, cargar_json_seguro
from core.autostart import habilitar_autostart, deshabilitar_autostart, autostart_activo
from core.i18n import t, establecer_idioma, obtener_idioma, IDIOMAS, MAPEO_FRECUENCIA, MAPEO_TEMAS

from core.paths import SETTINGS_FILE
from logger import log_error, log_warning


def cargar_ajustes():
    if os.path.exists(SETTINGS_FILE):
        try:
            return cargar_json_seguro(SETTINGS_FILE, valor_por_defecto={})
        except Exception:
            return {}
    return {}


def guardar_ajustes(data):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    try:
        return bool(guardar_json_atomico(SETTINGS_FILE, data))
    except Exception as error:
        log_error(f"No se pudieron guardar los ajustes: {error}", exc_info=True)
        return False


class SettingsModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("settings.title"))
        self.setFixedSize(560, 620)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        # Debe ser no modal: un QDialog modal hace que Windows bloquee el clic
        # exterior y emita el sonido de error antes de recibir el evento.
        self.setModal(False)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self._outside_click_filter_installed = False
        self.config_actual = cargar_ajustes()
        self.tema_original = config.CURRENT_THEME
        self.idioma_activo = obtener_idioma()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 18, 28, 20)
        layout.setSpacing(9)

        self.title = QLabel(t("settings.title"))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("dialogTitle")
        layout.addWidget(self.title)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setObjectName("separator")
        layout.addWidget(self.line)

        self.combos = {}

        def add_row(container, key, label_text, values, default_idx=0):
            row = QHBoxLayout()
            row.setContentsMargins(10, 4, 10, 4)
            label = QLabel(label_text)
            combo = QComboBox()
            combo.addItems(values)
            combo.setMinimumWidth(205)
            label.setToolTip(label_text)

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
            container.addLayout(row)
            self.combos[key] = combo

        def add_section(title_key):
            group = QGroupBox(t(title_key))
            group_layout = QVBoxLayout(group)
            group_layout.setContentsMargins(9, 9, 9, 8)
            group_layout.setSpacing(4)
            layout.addWidget(group)
            return group_layout

        appearance = add_section("settings.group.appearance")
        # 1. Frecuencia bilingüe
        lista_idiomas = list(IDIOMAS.values())
        idx_lang = 1 if self.idioma_activo == "en" else 0
        add_row(appearance, "idioma", t("settings.lang_label"), lista_idiomas, idx_lang)

        # 3. Tema bilingüe
        lista_temas = MAPEO_TEMAS.get(self.idioma_activo, MAPEO_TEMAS["es"])
        idx_tema = 1 if config.CURRENT_THEME == "light" else 0
        add_row(appearance, "tema", t("settings.theme_label"), lista_temas, idx_tema)
        self.combos["tema"].currentTextChanged.connect(self._al_cambiar_tema_en_vivo)

        monitoring = add_section("settings.group.monitoring")
        lista_freq = MAPEO_FRECUENCIA.get(self.idioma_activo, MAPEO_FRECUENCIA["es"])
        add_row(monitoring, "frecuencia_busqueda", t("settings.freq_label"), lista_freq, 1)

        behavior = add_section("settings.group.behavior")
        # 4. Iniciar con Windows
        row_auto = QHBoxLayout()
        row_auto.setContentsMargins(10, 4, 10, 4)
        row_auto.addWidget(QLabel(t("settings.autostart_label")))
        row_auto.addStretch()
        self.chk_autostart = QCheckBox()
        self._autostart_disponible = True
        try:
            autostart_habilitado = autostart_activo()
        except Exception as error:
            autostart_habilitado = False
            self._autostart_disponible = False
            log_warning(f"No se pudo consultar el inicio automático de Windows: {error}")
        self.chk_autostart.setChecked(autostart_habilitado)
        if not self._autostart_disponible:
            self.chk_autostart.setEnabled(False)
            self.chk_autostart.setToolTip(
                "No se pudo consultar esta opción por permisos de Windows."
            )
        row_auto.addWidget(self.chk_autostart)
        behavior.addLayout(row_auto)

        # 5. Notificaciones de escritorio
        row_notif = QHBoxLayout()
        row_notif.setContentsMargins(10, 4, 10, 4)
        row_notif.addWidget(QLabel(t("settings.notif_label")))
        row_notif.addStretch()
        self.chk_notif = QCheckBox()
        self.chk_notif.setChecked(self.config_actual.get("notificaciones_activas", True))
        row_notif.addWidget(self.chk_notif)
        monitoring.addLayout(row_notif)

        # 6. Música de fondo
        row_music = QHBoxLayout()
        row_music.setContentsMargins(10, 4, 10, 4)
        row_music.addWidget(QLabel(t("settings.music_label")))
        row_music.addStretch()
        self.chk_music = QCheckBox()
        self.chk_music.setChecked(self.config_actual.get("musica_activa", True))
        row_music.addWidget(self.chk_music)
        behavior.addLayout(row_music)

        # Al cerrar se puede salir de la aplicación o dejarla en la bandeja.
        row_close = QHBoxLayout()
        row_close.setContentsMargins(10, 4, 10, 4)
        row_close.addWidget(QLabel(t("settings.minimize_close_label")))
        row_close.addStretch()
        self.chk_minimize_on_close = QCheckBox()
        self.chk_minimize_on_close.setChecked(
            self.config_actual.get("minimizar_al_cerrar", False)
        )
        row_close.addWidget(self.chk_minimize_on_close)
        behavior.addLayout(row_close)

        layout.addStretch(1)

        self.btn_save = QPushButton(t("settings.save_btn"))
        self.btn_save.setObjectName("accentButton")
        self.btn_save.clicked.connect(self._guardar_y_cerrar)
        layout.addWidget(self.btn_save)

        self._aplicar_estilos_modal()

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
            position = event.globalPosition().toPoint()
            if not self.frameGeometry().contains(position):
                # No cerrar al seleccionar una opción de los desplegables: Qt
                # los presenta en una ventana emergente separada del diálogo.
                target = QApplication.widgetAt(position)
                combo_popup_windows = {
                    combo.view().window() for combo in self.combos.values()
                }
                if target and target.window() in combo_popup_windows:
                    return False
                self._cerrar_y_volver_a_principal()
        return super().eventFilter(watched, event)

    def _cerrar_y_volver_a_principal(self):
        """Cierra ajustes y deja la ventana principal visible y activa."""
        if not self.isVisible():
            return
        self.reject()
        parent = self.parentWidget()
        if parent is not None:
            QTimer.singleShot(0, parent.showNormal)
            QTimer.singleShot(0, parent.raise_)
            QTimer.singleShot(0, parent.activateWindow)

    def _aplicar_estilos_modal(self):
        es_claro = (config.CURRENT_THEME == "light")
        bg_dialog = "#E9EDF2" if es_claro else "#1E1E2E"
        panel = "#F1F3F6" if es_claro else "#252638"
        texto_color = "#303946" if es_claro else "#FFFFFF"
        combo_bg = "#E4E9F0" if es_claro else "#2A2A3A"
        borde_color = "#CFD7E2" if es_claro else "#3A3A50"
        separador = borde_color
        btn_bg = "#C6D6EA" if es_claro else "#6366F1"
        btn_hover = "#B9CCE3" if es_claro else "#4F46E5"
        btn_text = "#354E76" if es_claro else "#FFFFFF"

        self.setStyleSheet(f"""
            QDialog {{ background: {bg_dialog}; color: {texto_color}; }}
            QLabel {{ color: {texto_color}; font: 10pt 'Segoe UI'; }}
            #dialogTitle {{ font: bold 14pt 'Segoe UI'; }}
            #separator {{ color: {separador}; background: {separador}; max-height: 1px; }}
            QGroupBox {{ background: {panel}; color: {texto_color}; border: 1px solid {borde_color}; border-radius: 9px; margin-top: 8px; padding-top: 7px; font: bold 9pt 'Segoe UI'; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 5px; }}
            QComboBox {{ background: {combo_bg}; color: {texto_color}; border: 1px solid {borde_color}; padding: 5px; border-radius: 4px; }}
            QComboBox QAbstractItemView {{ background: {bg_dialog}; color: {texto_color}; selection-background-color: {btn_bg}; }}
            QCheckBox {{ color: {texto_color}; }}
            #accentButton {{ background: {btn_bg}; color: {btn_text}; border: 1px solid {btn_bg}; font: bold 10pt 'Segoe UI'; padding: 10px; border-radius: 7px; }}
            #accentButton:hover {{ background: {btn_hover}; border-color: {btn_hover}; }}
            #accentButton:pressed {{ background: {'#555BB5' if es_claro else '#4338CA'}; }}
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
        nuevos_ajustes = dict(self.config_actual)
        nuevos_ajustes["frecuencia_busqueda"] = self.combos["frecuencia_busqueda"].currentText()
        nuevos_ajustes["idioma"] = idioma_seleccionado_txt
        nuevos_ajustes["idioma_codigo"] = lang_code
        nuevos_ajustes["tema"] = tema_elegido_txt
        nuevos_ajustes["tema_clave"] = tema_clave
        nuevos_ajustes["notificaciones_activas"] = self.chk_notif.isChecked()
        nuevos_ajustes["musica_activa"] = self.chk_music.isChecked()
        nuevos_ajustes["minimizar_al_cerrar"] = self.chk_minimize_on_close.isChecked()
        if not guardar_ajustes(nuevos_ajustes):
            QMessageBox.warning(
                self,
                t("settings.title"),
                t("settings.save_error"),
            )
            return

        self.config_actual = nuevos_ajustes
        establecer_idioma(lang_code)

        if self._autostart_disponible and self.chk_autostart.isChecked():
            try:
                if not habilitar_autostart():
                    log_warning("No se pudo aplicar el inicio automático de Windows.")
            except Exception as error:
                log_warning(f"No se pudo activar el inicio con Windows: {error}")
        elif self._autostart_disponible:
            try:
                if not deshabilitar_autostart():
                    log_warning("No se pudo quitar el inicio automático de Windows.")
            except Exception as error:
                log_warning(f"No se pudo desactivar el inicio con Windows: {error}")

        parent = self.parent()
        if parent:
            if hasattr(parent, "aplicar_preferencia_musica"):
                parent.aplicar_preferencia_musica(nuevos_ajustes["musica_activa"])
            if hasattr(parent, "_actualizar_textos_idioma"):
                parent._actualizar_textos_idioma()
            if hasattr(parent, "_tray") and parent._tray:
                parent._tray.actualizar_temporizador_busqueda()

        self.accept()

    def reject(self):
        if config.CURRENT_THEME != self.tema_original:
            self._sincronizar_tema_nativo(self.tema_original)
        super().reject()
