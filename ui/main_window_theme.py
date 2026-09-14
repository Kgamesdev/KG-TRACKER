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
  QToolTip {{
    background: {c("COLOR_BG_CARD")};
    color: {c("COLOR_TEXT_PRIMARY")};
    border: 1px solid {c("COLOR_ACCENT")};
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 8pt;
    font-family: "Segoe UI";
  }}

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

  /* TARJETA DE JUEGO GAMING */
  QFrame#gameCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {c("COLOR_BG_CARD")}, stop:1 #1C1D2E);
    border: 1px solid {c("COLOR_BORDER")};
    border-radius: 12px;
  }}

  QFrame#gameCard:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #383952, stop:1 #222338);
    border: 1px solid rgba(129, 140, 248, 0.75);
  }}

  QLabel#gameImage {{
    background: {c("COLOR_BG_DESC")};
    color: {c("COLOR_TEXT_MUTED")};
    font: bold 8pt "Segoe UI";
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }}

  QLabel#gameTitle {{
    color: {c("COLOR_TEXT_PRIMARY")};
    font: bold 11.5pt "Segoe UI";
    padding-bottom: 1px;
  }}

  QLabel#gameDescription {{
    color: {c("COLOR_TEXT_SECONDARY")};
    font: 8.5pt "Segoe UI";
    line-height: 1.2;
  }}

  /* CHIPS / CÁPSULAS UNIFORMES */
  QLabel#gameStore {{
    background-color: rgba(99, 102, 241, 0.18);
    color: #A5B4FC;
    border: 1px solid #818CF8;
    border-radius: 6px;
    padding: 2px 8px;
    font: bold 7.5pt "Segoe UI";
  }}

  QLabel#gameWorth {{
    background-color: rgba(245, 158, 11, 0.18);
    color: #FCD34D;
    border: 1px solid #F59E0B;
    border-radius: 6px;
    padding: 2px 8px;
    font: bold 7.5pt "Segoe UI";
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

  /* BOTONES DE LA BARRA LATERAL */
  QPushButton[role="sidebar"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {c("COLOR_SIDEBAR_HOVER")}, stop:1 {c("COLOR_SIDEBAR")});
    color: {c("COLOR_TEXT_PRIMARY")};
    border: 1px solid {c("COLOR_BORDER")};
    border-radius: 12px;
  }}

  QPushButton[role="sidebar"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {c("COLOR_ACCENT_LIGHT")}, stop:1 {c("COLOR_ACCENT")});
    border: 1px solid {c("COLOR_ACCENT_LIGHT")};
    border-bottom: 2px solid {c("COLOR_ACCENT_HOVER")};
  }}

  QPushButton[role="sidebar"]:pressed {{
    background: {c("COLOR_ACCENT_HOVER")};
    border: 1px solid {c("COLOR_ACCENT")};
    border-top: 2px solid rgba(0, 0, 0, 0.5);
    padding-top: 3px;
  }}

  /* BOTÓN PRINCIPAL */
  QPushButton[role="accent"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366F1, stop:1 #4F46E5);
    color: #FFFFFF;
    border: 1.2px solid #818CF8;
    border-radius: 12px;
    font-weight: bold;
    font-size: 9.5pt;
    letter-spacing: 0.5px;
  }}

  QPushButton[role="accent"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #818CF8, stop:1 #6366F1);
    border: 1.2px solid #00F3FF;
  }}

  QPushButton[role="accent"]:pressed {{
    background: #4338CA;
    border-top: 2px solid rgba(0, 0, 0, 0.4);
    padding-top: 2px;
  }}

  /* BOTÓN RECLAMAR */
  QPushButton[role="success"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10B981, stop:1 #059669);
    color: #FFFFFF;
    border: 1px solid #34D399;
    border-radius: 11px;
    font-weight: bold;
    font-size: 8pt;
  }}

  QPushButton[role="success"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34D399, stop:1 #10B981);
    border: 1px solid #6EE7B7;
  }}

  QPushButton[role="success"]:pressed {{
    background: #047857;
    border: 1px solid #065F46;
    padding-top: 2px;
  }}

  /* BOTONES SECUNDARIOS [ ✔ ] y [ 🔗 ] */
    QPushButton[role="secondary"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {c("COLOR_BG_CARD")}, stop:1 {c("COLOR_BG_DESC")});
    color: {c("COLOR_TEXT_PRIMARY")};
    border: 1px solid {c("COLOR_BORDER")};
    border-radius: 10px;
    font-weight: bold;
    font-size: 8.5pt;
  }}

  QPushButton[role="secondary"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4E506B, stop:1 #3A3B52);
    border: 1px solid #818CF8;
    color: #818CF8;
  }}

  QPushButton[role="secondary"]:pressed {{
    background: #1E1F2E;
    border: 1px solid #3A3B52;
    padding-top: 2px;
  }}

  QScrollArea {{
    background: transparent;
    border: none;
  }}

  QScrollBar:vertical {{
    background: rgba(23, 24, 39, 0.45);
    width: 10px;
    margin: 2px 2px 2px 2px;
    border-radius: 5px;
  }}

  QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c("COLOR_ACCENT")}, stop:1 {c("COLOR_ACCENT_LIGHT")});
    min-height: 32px;
    border-radius: 4px;
    border: 1px solid rgba(129, 140, 248, 0.35);
  }}

  QScrollBar::handle:vertical:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c("COLOR_ACCENT_LIGHT")}, stop:1 #00F3FF);
    border: 1.5px solid #00F3FF;
  }}

  QScrollBar::handle:vertical:pressed {{
    background: #00F3FF;
    border: 1.5px solid #FFFFFF;
  }}

  QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
    width: 0px;
    background: transparent;
    border: none;
  }}

  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
    border: none;
  }}

  /* BANNER INFORMATIVO CENTRADO RESPLANDECIENTE DE CONTEXTO DE TIENDA */
    QFrame#storeContextBanner {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c("COLOR_BG_CARD")}, stop:0.5 {c("COLOR_BG_DESC")}, stop:1 {c("COLOR_BG_CARD")});
    border: 1px solid {c("COLOR_BORDER")};
    border-radius: 10px;
  }}

  QLabel#storeContextTitle {{
    color: {c("COLOR_TEXT_PRIMARY")};
    font: bold 9.5pt "Segoe UI";
    letter-spacing: 0.8px;
    background: transparent;
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
    border: none;
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

  self._actualizar_estilo_botones()
  if hasattr(self, "_actualizar_vista_juegos"):
      self._actualizar_vista_juegos()


def _actualizar_estilo_botones(self):
  self._set_button_role(self.btn_side_back, "sidebar")
  self._set_button_role(self.btn_side_kofi, "sidebar")
  self._set_button_role(self.btn_side_settings, "sidebar")
  self._set_button_role(self.btn_side_theme, "sidebar")
  self._set_button_role(self.btn_side_todas, "accent")
  self._set_button_role(self.btn_actualizar, "accent")
  self._set_button_role(self.btn_reclamados, "secondary")
  if hasattr(self, "ahorro_pill") and self.ahorro_pill is not None:
      self.ahorro_pill.setProperty("role", "saved_pill")
      self.ahorro_pill.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E5A93C, stop:1 #C8861E); color: #FFFFFF; border: 1.5px solid #FAD06C; border-radius: 12px; padding: 0 8px; font-weight: bold; }")
      self.ahorro_pill.style().unpolish(self.ahorro_pill)
      self.ahorro_pill.style().polish(self.ahorro_pill)
  self._set_button_role(self.btn_mute, "secondary")


def _set_button_role(self, button, role):
  if button is None:
    return
  button.setProperty("role", role)
  if hasattr(button, "aplicar_estilo_segun_rol"):
      button.aplicar_estilo_segun_rol()
  button.style().unpolish(button)
  button.style().polish(button)


def instalar_metodos(cls):
  cls._apply_theme_qss = _apply_theme_qss
  cls._sync_theme_properties = _sync_theme_properties
  cls.alternar_tema = alternar_tema
  cls._actualizar_estilo_botones = _actualizar_estilo_botones
  cls._set_button_role = _set_button_role
