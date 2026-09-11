"""Tema QSS y sincronización visual de la ventana principal."""

import config
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from config import (
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER, COLOR_WARNING, COLOR_ERROR,
    COLOR_SIDEBAR, COLOR_TEXT_PRIMARY,
)


def _apply_theme_qss(self):
    tema = config.THEMES[config.CURRENT_THEME]

    def c(name):
        return tema[name]

    qss = f"""
    QMainWindow, QWidget#rootFrame {{
        background: {c("COLOR_BG")};
        color: {c("COLOR_TEXT_PRIMARY")};
    }}

    QFrame#sidebar {{
        background: {c("COLOR_SIDEBAR")};
    }}

    QFrame#storePanel {{
        background: {c("COLOR_BG_CARD")};
        border: 1px solid {c("COLOR_BORDER")};
        border-radius: 12px;
    }}

    QFrame#storeBubble {{
        background: transparent;
        border: none;
        border-radius: 0px;
    }}

    QFrame#storeIconBox {{
        background: {c("COLOR_BG_CARD")};
        border: none;
        border-radius: 0px;
    }}

    QFrame#storeBubble[hovering="true"] QFrame#storeIconBox {{
        background: {c("COLOR_ACCENT_LIGHT")};
    }}

    QLabel#storeLabel {{
        color: {c("COLOR_TEXT_PRIMARY")};
        background: transparent;
        font: bold 8pt "Segoe UI";
    }}
    QFrame#storeBubble[hovering="true"] QLabel#storeLabel {{
        color: {c("COLOR_ACCENT_LIGHT")};
    }}
    QFrame#storeBubble[active="true"] QLabel#storeLabel {{
        color: {c("COLOR_SUCCESS")};
    }}
    QLabel#storeBadge {{
        background: {c("COLOR_ERROR")};
        color: white;
        border-radius: 8px;
        min-width: 16px;
        max-width: 16px;
        min-height: 16px;
        max-height: 16px;
        font: bold 8pt "Segoe UI";
    }}

    QFrame#gameCard {{
        background: {c("COLOR_BG_CARD")};
        border: 1px solid {c("COLOR_BORDER")};
        border-radius: 0px;
    }}

    QLabel#gameImage {{
        background: {c("COLOR_BG_DESC")};
        color: {c("COLOR_TEXT_MUTED")};
        font: bold 8pt "Segoe UI";
    }}

    QLabel#gameTitle {{
        color: {c("COLOR_TEXT_PRIMARY")};
        font: bold 11pt "Segoe UI";
    }}

    QLabel#gameDescription {{
        color: {c("COLOR_TEXT_SECONDARY")};
        font: 8pt "Segoe UI";
    }}

    QLabel#gameStore {{
        color: {c("COLOR_ACCENT_LIGHT")};
        font: bold 7pt "Segoe UI";
    }}

    QLabel#gameWorth {{
        color: {c("COLOR_SUCCESS")};
        font: bold 7pt "Segoe UI";
    }}

    QLabel#statusPill {{
        background: {c("COLOR_BG_CARD")};
        color: {c("COLOR_SUCCESS")};
        padding: 6px 12px;
        border-radius: 8px;
        font: bold 9pt "Segoe UI";
    }}

    QLabel#statusPill[status="warning"] {{ color: {c("COLOR_WARNING")}; }}
    QLabel#statusPill[status="error"] {{ color: {c("COLOR_ERROR")}; }}
    QLabel#statusPill[status="success"] {{ color: {c("COLOR_SUCCESS")}; }}
    QLabel#statusPill[status="accent"] {{ color: {c("COLOR_ACCENT_LIGHT")}; }}

    QPushButton[role="saving"] {{
        background: {c("COLOR_BG_CARD")};
        color: {c("COLOR_WARNING")};
        border: 1px solid {c("COLOR_BORDER")};
    }}
    QPushButton[role="saving"]:hover {{
        background: {c("COLOR_HOVER")};
    }}

    QPushButton {{
        font-family: "Segoe UI";
    }}

    QPushButton[role="sidebar"] {{
        background: {c("COLOR_SIDEBAR")};
        color: {c("COLOR_TEXT_PRIMARY")};
        border: 1px solid {c("COLOR_BORDER")};
    }}
    QPushButton[role="sidebar"]:hover {{
        background: {c("COLOR_ACCENT")};
    }}

    QPushButton[role="accent"] {{
        background: {c("COLOR_ACCENT")};
        color: white;
        border: 1px solid {c("COLOR_ACCENT")};
    }}
    QPushButton[role="accent"]:hover {{
        background: {c("COLOR_ACCENT_HOVER")};
    }}

    QPushButton[role="success"] {{
        background: {c("COLOR_SUCCESS")};
        color: white;
        border: 1px solid {c("COLOR_SUCCESS")};
    }}
    QPushButton[role="success"]:hover {{
        background: {c("COLOR_SUCCESS_HOVER")};
    }}

    QPushButton[role="secondary"] {{
        background: {c("COLOR_BG_CARD")};
        color: {c("COLOR_ACCENT_LIGHT")};
        border: 1px solid {c("COLOR_BORDER")};
    }}
    QPushButton[role="secondary"]:hover {{
        background: {c("COLOR_HOVER")};
    }}

    QScrollArea {{
        background: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background: {c("COLOR_BG")};
        width: 10px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {c("COLOR_BORDER")};
        min-height: 30px;
        border-radius: 5px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QFrame#storeHeader {{
        background: {c("COLOR_BG_CARD")};
    }}

    QPushButton#storeHeaderButton {{
        background: transparent;
        color: {c("COLOR_TEXT_PRIMARY")};
        border: none;
        text-align: left;
        padding: 10px 14px;
        font: bold 10pt "Segoe UI";
    }}

    QLabel#offerCount {{
        color: {c("COLOR_ACCENT_LIGHT")};
        background: transparent;
        font: bold 8pt "Segoe UI";
        padding: 0 14px;
    }}

    QLabel#emptyLabel {{
        color: {c("COLOR_TEXT_MUTED")};
        background: transparent;
        font: italic 9pt "Segoe UI";
    }}

    QLabel#volumeLabel {{
        color: {c("COLOR_TEXT_MUTED")};
        background: transparent;
        font: bold 8pt "Segoe UI";
    }}

    QSlider {{
        background: transparent;
    }}
    QSlider::groove:horizontal {{
        height: 5px;
        background: {c("COLOR_BORDER")};
        border-radius: 2px;
    }}
    QSlider::sub-page:horizontal {{
        background: {c("COLOR_ACCENT")};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        width: 14px;
        margin: -5px 0;
        border-radius: 7px;
        background: {c("COLOR_TEXT_PRIMARY")};
        border: 2px solid {c("COLOR_ACCENT")};
    }}
    """
    self.setStyleSheet(qss)
    self._sync_theme_properties()



def _sync_theme_properties(self):
    for store, widget in self.bubble_widgets.items():
        widget.setProperty("active", bool(self.active_filters.get(store, False)))
        widget.style().unpolish(widget)
        widget.style().polish(widget)



def alternar_tema(self):
    """Cambia el tema en caliente aplicando un QSS global."""
    config.CURRENT_THEME = "light" if config.CURRENT_THEME == "dark" else "dark"
    self.es_modo_oscuro = config.CURRENT_THEME == "dark"
    self._apply_theme_qss()

    icon_path = self._icon_path(
        "light_theme.png" if self.es_modo_oscuro else "dark_theme.png"
    )
    self.btn_side_theme.setIcon(QIcon(icon_path))
    self.btn_side_theme.setIconSize(QSize(28, 28))

    # QSS actualiza todos los widgets existentes. No se reconstruye
    # rootFrame, no se elimina el árbol y no se vuelve a consultar la API.
    self._actualizar_estilo_botones()



def _actualizar_estilo_botones(self):
    self._set_button_role(self.btn_side_back, "sidebar")
    self._set_button_role(self.btn_side_kofi, "sidebar")
    self._set_button_role(self.btn_side_settings, "sidebar")
    self._set_button_role(self.btn_side_theme, "sidebar")
    self._set_button_role(self.btn_side_todas, "accent")
    self._set_button_role(self.btn_actualizar, "accent")
    self._set_button_role(self.btn_reclamados, "secondary")
    self._set_button_role(self.ahorro_pill, "secondary")
    self._set_button_role(self.btn_mute, "secondary")



def _set_button_role(self, button, role):
    if button is None:
        return
    button.setProperty("role", role)
    button.style().unpolish(button)
    button.style().polish(button)



def instalar_metodos(cls):

    cls._apply_theme_qss = _apply_theme_qss

    cls._sync_theme_properties = _sync_theme_properties

    cls.alternar_tema = alternar_tema

    cls._actualizar_estilo_botones = _actualizar_estilo_botones

    cls._set_button_role = _set_button_role
