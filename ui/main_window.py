"""Interfaz principal de K GAME TRACKER basada en PySide6/Qt.

La capa de datos, estado, filtrado, API y audio conserva la lógica
existente de la aplicación. El tema se aplica en caliente mediante
una hoja QSS global, sin reconstruir la ventana principal.
"""

import hashlib
import json
import os
import re
import sys
import webbrowser
from datetime import datetime

import pygame
import requests

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

import config
from config import (
    API_URL, API_HEADERS, EXCLUSIONES, STORES_MAPPING,
    COLOR_BG, COLOR_BG_CARD, COLOR_BG_DESC, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER, COLOR_WARNING, COLOR_ERROR,
    COLOR_SIDEBAR, COLOR_SIDEBAR_HOVER, COLOR_BORDER, COLOR_HOVER,
    WINDOW_TITLE, ICON_PATH, THUMBNAIL_SIZE, AUDIO_PATH,
    LOGO_PATH,
)
from core.images import limpiar_cache_imagenes
from ui.kofi_modal import KofiModal
from ui.settings_modal import SettingsModal


class RoundedButton(QPushButton):
    """Botón Qt equivalente al RoundedButton original."""

    def __init__(
        self,
        parent=None,
        text="",
        command=None,
        width=120,
        height=42,
        bg=COLOR_BG_CARD,
        hover_bg=COLOR_HOVER,
        fg="white",
        radius=12,
        font=("Segoe UI", 9, "bold"),
        border=COLOR_BORDER,
        border_width=1,
        icon_path=None,
        icon_size=(20, 20),
        role="default",
    ):
        super().__init__(text, parent)
        self._bg = bg
        self._hover = hover_bg
        self._fg = fg
        self._border = border
        self._border_width = border_width
        self._radius = radius
        self._command = command
        self._icon_path = icon_path
        self._icon_size = icon_size
        self._role = role

        self.setFixedSize(int(width), int(height))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setFont(self._qfont(font))
        self.setProperty("role", role)
        self.set_colors(bg, hover_bg, fg, border)
        self.set_icon(icon_path)

        if callable(command):
            self.clicked.connect(command)

    @staticmethod
    def _qfont(font):
        from PySide6.QtGui import QFont
        family = font[0] if font else "Segoe UI"
        size = int(font[1]) if len(font) > 1 else 9
        qfont = QFont(family, size)
        if len(font) > 2 and str(font[2]).lower() == "bold":
            qfont.setBold(True)
        return qfont

    def set_icon(self, icon_path):
        self._icon_path = icon_path
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(*self._icon_size))
        else:
            self.setIcon(QIcon())

    def set_colors(self, bg=None, hover=None, fg=None, border=None):
        if bg is not None:
            self._bg = bg
        if hover is not None:
            self._hover = hover
        if fg is not None:
            self._fg = fg
        if border is not None:
            self._border = border
        self._apply_inline_style()

    def _apply_inline_style(self):
        self.setStyleSheet(
            f"QPushButton {{ background: {self._bg}; color: {self._fg}; "
            f"border: {self._border_width}px solid {self._border}; "
            f"border-radius: {self._radius}px; padding: 0 8px; }}"
            f"QPushButton:hover {{ background: {self._hover}; }}"
        )

    def config(self, **kwargs):
        if "text" in kwargs:
            self.setText(kwargs.pop("text"))
        if "bg" in kwargs:
            self._bg = kwargs.pop("bg")
        if "fg" in kwargs:
            self._fg = kwargs.pop("fg")
        if "activebackground" in kwargs:
            self._hover = kwargs.pop("activebackground")
        if "font" in kwargs:
            self.setFont(self._qfont(kwargs.pop("font")))
        self._apply_inline_style()
        if kwargs.get("enabled") is not None:
            self.setEnabled(kwargs.pop("enabled"))
        if kwargs:
            for key, value in kwargs.items():
                try:
                    setattr(self, key, value)
                except Exception:
                    pass


class VolumeSlider(QSlider):
    """Slider Qt equivalente al control de volumen original."""

    def __init__(self, parent=None, from_=0, to=100, length=120, command=None, **kwargs):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self._command = command
        self.setRange(int(from_), int(to))
        self.setFixedWidth(int(length))
        self.setFixedHeight(22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value):
        if callable(self._command):
            self._command(value)

    def set_colors(self, bg=None, track_bg=None, fill_bg=None, knob_bg=None):
        self.setStyleSheet(
            f"QSlider {{ background: {bg or 'transparent'}; }}"
            f"QSlider::groove:horizontal {{ height: 5px; background: {track_bg or COLOR_BORDER}; border-radius: 2px; }}"
            f"QSlider::sub-page:horizontal {{ background: {fill_bg or COLOR_ACCENT}; border-radius: 2px; }}"
            f"QSlider::handle:horizontal {{ width: 14px; margin: -5px 0; border-radius: 7px; background: {knob_bg or COLOR_TEXT_PRIMARY}; border: 2px solid {fill_bg or COLOR_ACCENT}; }}"
        )


class GameCard(QFrame):
    """Tarjeta Qt de un juego."""

    def __init__(self, owner, juego, nombre_tienda):
        super().__init__(owner.frame_lista)
        self.owner = owner
        self.juego = juego
        self.nombre_tienda = nombre_tienda
        self.setObjectName("gameCard")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 12, 10)
        layout.setSpacing(10)

        image_box = QLabel()
        image_box.setObjectName("gameImage")
        image_box.setFixedSize(190, 104)
        image_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label = image_box
        layout.addWidget(image_box)

        info = QVBoxLayout()
        info.setSpacing(4)

        title = QLabel(str(juego.get("title", "Elemento sin título")))
        title.setObjectName("gameTitle")
        title.setWordWrap(True)
        info.addWidget(title)

        descripcion = " ".join(str(juego.get("description", "Sin descripción disponible.")).split())
        if len(descripcion) > 170:
            descripcion = descripcion[:167] + "..."
        desc = QLabel(descripcion)
        desc.setObjectName("gameDescription")
        desc.setWordWrap(True)
        info.addWidget(desc)

        store = QLabel(nombre_tienda.upper())
        store.setObjectName("gameStore")
        info.addWidget(store)

        valor = owner._valor_juego(juego)
        if valor > 0:
            worth = QLabel(f"VALOR ESTIMADO: ${valor:,.2f}")
            worth.setObjectName("gameWorth")
            info.addWidget(worth)

        info.addStretch()
        layout.addLayout(info, 1)

        actions = QVBoxLayout()
        actions.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if owner._esta_reclamado(juego):
            btn = RoundedButton(
                self, text="✓ RECLAMADO",
                command=lambda j=juego: owner._alternar_reclamado(j),
                width=128, height=38,
                bg=COLOR_ACCENT, hover_bg=COLOR_ACCENT_HOVER,
                fg="white", border=COLOR_ACCENT, radius=11,
                font=("Segoe UI", 8, "bold"), role="accent",
            )
            actions.addWidget(btn)
        else:
            btn_reclamar = RoundedButton(
                self, text="RECLAMAR",
                command=lambda u=str(juego.get("open_giveaway_url") or ""): owner._abrir_reclamacion(u),
                width=128, height=36,
                bg=COLOR_SUCCESS, hover_bg=COLOR_SUCCESS_HOVER,
                fg="white", border=COLOR_SUCCESS, radius=11,
                font=("Segoe UI", 8, "bold"),
                icon_path=owner._action_icon_path("open_link.png"),
                icon_size=(18, 18), role="success",
            )
            actions.addWidget(btn_reclamar)
            btn_marcar = RoundedButton(
                self, text="★ RECLAMADO",
                command=lambda j=juego: owner._alternar_reclamado(j),
                width=128, height=32,
                bg=COLOR_BG_CARD, hover_bg=COLOR_HOVER,
                fg=COLOR_ACCENT_LIGHT, border=COLOR_BORDER, radius=10,
                font=("Segoe UI", 7, "bold"), role="secondary",
            )
            actions.addWidget(btn_marcar)

        layout.addLayout(actions)

        self._load_image(juego.get("image") or juego.get("thumbnail"))

    def _load_image(self, url_img):
        pixmap = self.owner._load_thumbnail(url_img)
        if pixmap is not None and not pixmap.isNull():
            self._image_label.setPixmap(
                pixmap.scaled(
                    self._image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self._image_label.setText("SIN\nMINIATURA")


class StoreWidget(QFrame):
    """Burbuja de tienda con la geometría visual de la versión Tk original."""

    def __init__(self, owner, store, icon_filename):
        super().__init__(owner.store_panel)
        self.owner = owner
        self.store = store
        self.setObjectName("storeBubble")
        self.setProperty("active", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 10, 6, 12)
        layout.setSpacing(4)

        self.icon_box = QFrame()
        self.icon_box.setObjectName("storeIconBox")
        self.icon_box.setFixedSize(80, 80)
        icon_layout = QVBoxLayout(self.icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)

        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path = owner._store_icon_path(icon_filename)
        pixmap = owner._load_store_icon(path, 64)
        if pixmap is not None:
            icon.setPixmap(pixmap)
        icon_layout.addWidget(icon)
        self.icon_label = icon

        layout.addWidget(self.icon_box, 0, Qt.AlignmentFlag.AlignHCenter)

        self.badge = QLabel("0", self.icon_box)
        self.badge.setObjectName("storeBadge")
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge.setGeometry(62, 6, 16, 16)
        self.badge.hide()

        label = QLabel(store)
        label.setObjectName("storeLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.label = label

    def _refresh_state(self):
        for widget in (self, self.icon_box, self.label):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def enterEvent(self, event):
        self.setProperty("hovering", True)
        self._refresh_state()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovering", False)
        self._refresh_state()
        super().leaveEvent(event)

    def set_count(self, count):
        self.badge.setText(str(count))
        self.badge.setVisible(int(count) > 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.owner._toggle_tienda(self.store)
        super().mousePressEvent(event)


class VentanaPrincipal(QMainWindow):
    """Ventana principal de K GAME TRACKER."""

    def __init__(self, parent=None, al_cerrar_app=None, mostrar=True):
        super().__init__(parent if isinstance(parent, QWidget) else None)
        self.parent = parent
        self.al_cerrar_app = al_cerrar_app

        # Alias de compatibilidad con el código existente.
        self.ventana = self

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(980, 360)
        self.resize(1120, 360)
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.es_modo_oscuro = config.CURRENT_THEME == "dark"
        self.audio_silenciado = False
        self.volumen_anterior = 20
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
        if mostrar:
            self.show()

    # ------------------------------------------------------------------
    # QSS / TEMA
    # ------------------------------------------------------------------

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

    @staticmethod
    def _set_button_role(button, role):
        if button is None:
            return
        button.setProperty("role", role)
        button.style().unpolish(button)
        button.style().polish(button)

    # ------------------------------------------------------------------
    # CONSTRUCCIÓN
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("rootFrame")
        self.setCentralWidget(root)

        main_layout = QGridLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setHorizontalSpacing(0)
        main_layout.setVerticalSpacing(0)
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(74)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(5, 0, 5, 10)
        sidebar_layout.setSpacing(5)
        main_layout.addWidget(self.sidebar, 0, 0, 2, 1)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFixedSize(64, 64)
        sidebar_layout.addSpacing(16)
        logo.setCursor(Qt.CursorShape.PointingHandCursor)
        logo_pixmap = self._load_store_icon(LOGO_PATH, 64)
        if logo_pixmap is not None:
            logo.setPixmap(logo_pixmap)
        else:
            logo.setText("K\nG")
        logo.mousePressEvent = lambda event: self.resetear_app()
        self.logo_btn = logo
        sidebar_layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignHCenter)
        sidebar_layout.addSpacing(12)

        # Acciones contextuales: siempre quedan justo debajo del logo.
        # No se usa un contenedor con stretch porque eso las centraba
        # verticalmente en la sidebar.
        self.btn_side_todas = RoundedButton(
            self.sidebar, command=self.toggle_todas,
            width=54, height=50, bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER, radius=13,
            role="sidebar",
        )
        self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
        self.btn_side_todas.setIconSize(QSize(28, 28))
        self.btn_side_todas.setToolTip("Seleccionar todas")
        self.btn_side_todas.hide()
        sidebar_layout.addWidget(
            self.btn_side_todas, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.btn_side_back = RoundedButton(
            self.sidebar, command=self.volver_atras,
            width=54, height=50, bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER, radius=13,
            icon_path=self._icon_path("back.png"), icon_size=(28, 28),
            role="sidebar",
        )
        self.btn_side_back.hide()
        sidebar_layout.addWidget(
            self.btn_side_back, 0, Qt.AlignmentFlag.AlignHCenter
        )

        # El stretch queda después de las acciones: empuja solo el bloque
        # inferior hacia abajo.
        sidebar_layout.addStretch(1)

        self.sidebar_bottom = QWidget()
        bottom_sidebar_layout = QVBoxLayout(self.sidebar_bottom)
        bottom_sidebar_layout.setContentsMargins(0, 0, 0, 0)
        bottom_sidebar_layout.setSpacing(5)
        sidebar_layout.addWidget(self.sidebar_bottom, 0)

        self.btn_side_kofi = RoundedButton(
            self.sidebar_bottom, command=self._abrir_kofi,
            width=54, height=50, bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER, radius=13,
            icon_path=self._icon_path("cafe.png"), icon_size=(28, 28),
            role="sidebar",
        )
        bottom_sidebar_layout.addWidget(self.btn_side_kofi, 0, Qt.AlignmentFlag.AlignHCenter)

        self.btn_side_settings = RoundedButton(
            self.sidebar_bottom, command=self._abrir_settings,
            width=54, height=50, bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER, radius=13,
            icon_path=self._icon_path("settings.png"), icon_size=(28, 28),
            role="sidebar",
        )
        bottom_sidebar_layout.addWidget(self.btn_side_settings, 0, Qt.AlignmentFlag.AlignHCenter)

        self.btn_side_theme = RoundedButton(
            self.sidebar_bottom, command=self.alternar_tema,
            width=54, height=50, bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER, radius=13,
            icon_path=self._icon_path(
                "light_theme.png" if self.es_modo_oscuro else "dark_theme.png"
            ),
            icon_size=(28, 28), role="sidebar",
        )
        bottom_sidebar_layout.addWidget(self.btn_side_theme, 0, Qt.AlignmentFlag.AlignHCenter)

        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(28, 16, 28, 14)
        content_layout.setSpacing(0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.content, 0, 1)

        self.store_panel = QFrame()
        self.store_panel.setObjectName("storePanel")
        self.store_panel.setFixedHeight(180)
        self.store_layout = QGridLayout(self.store_panel)
        self.store_layout.setContentsMargins(0, 0, 0, 0)
        self.store_layout.setHorizontalSpacing(0)
        self.store_layout.setVerticalSpacing(0)
        content_layout.addWidget(self.store_panel)
        content_layout.addSpacing(16)

        self._crear_burbujas_tiendas()

        self.btn_actualizar = RoundedButton(
            self.content, text="BUSCAR JUEGOS GRATUITOS",
            command=self.buscar_juegos, height=50,
            width=100, bg=COLOR_ACCENT, hover_bg=COLOR_ACCENT_HOVER,
            fg="white", border=COLOR_ACCENT, radius=14,
            font=("Segoe UI", 11, "bold"), role="accent",
        )
        # Este botón ocupa todo el ancho disponible.
        self.btn_actualizar.setMinimumWidth(0)
        self.btn_actualizar.setMaximumWidth(16777215)
        self.btn_actualizar.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        content_layout.addWidget(self.btn_actualizar)
        content_layout.addSpacing(12)

        self.container = QWidget()
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.scrollbar = None
        self.canvas = QScrollArea()
        self.canvas.setObjectName("gamesScroll")
        self.canvas.setWidgetResizable(True)
        self.canvas.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.canvas.setAutoFillBackground(False)
        self.canvas.viewport().setAutoFillBackground(False)
        self.canvas.viewport().setStyleSheet("background: transparent; border: none;")

        self.frame_lista = QWidget()
        self.frame_lista.setObjectName("gamesList")
        self.frame_lista.setAutoFillBackground(False)
        self.frame_lista_layout = QVBoxLayout(self.frame_lista)
        self.frame_lista_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_lista_layout.setSpacing(4)
        self.frame_lista_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.canvas.setWidget(self.frame_lista)

        container_layout.addWidget(self.canvas)
        content_layout.addWidget(self.container, 0)
        # Mientras no haya juegos, este panel no participa en la distribucion
        # vertical. La cabecera queda fija arriba.
        self.container.hide()
        content_layout.addSpacing(8)

        # La barra inferior tiene una fila propia en la ventana raíz.
        # No se desplaza cuando la zona de juegos aparece o desaparece.

        self.bottom = QWidget()
        bottom_layout = QHBoxLayout(self.bottom)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        self.status_pill = RoundedButton(
            self.bottom, text="● LISTO",
            width=88, height=34, bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER, fg=COLOR_SUCCESS,
            border=COLOR_BORDER, radius=10,
            font=("Segoe UI", 8, "bold"), role="secondary",
        )
        bottom_layout.addWidget(self.status_pill)

        self.btn_reclamados = RoundedButton(
            self.bottom, text="★ RECLAMADOS",
            command=self.mostrar_reclamados,
            width=142, height=34, bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER, fg=COLOR_ACCENT_LIGHT,
            border=COLOR_BORDER, radius=10,
            font=("Segoe UI", 8, "bold"), role="secondary",
        )
        bottom_layout.addWidget(self.btn_reclamados)

        self.ahorro_pill = RoundedButton(
            self.bottom, text="$ AHORRADO : 0.00",
            width=156, height=34, bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER,
            fg=(COLOR_WARNING if config.CURRENT_THEME == "light" else "#F2C94C"),
            border=COLOR_BORDER, radius=10,
            font=("Segoe UI", 8, "bold"), role="saving",
        )
        bottom_layout.addWidget(self.ahorro_pill)
        self._actualizar_contador_ahorrado()

        bottom_layout.addStretch()

        volume_label = QLabel("VOLUMEN")
        volume_label.setObjectName("volumeLabel")
        bottom_layout.addWidget(volume_label)

        self.slider_volumen = VolumeSlider(
            self.bottom, from_=0, to=100, length=120,
            command=self.cambiar_volumen,
        )
        self.slider_volumen.setValue(20)
        bottom_layout.addWidget(self.slider_volumen)

        self.btn_mute = RoundedButton(
            self.bottom, command=self.alternar_mute,
            width=42, height=38, bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER, fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER, radius=11,
            icon_path=self._icon_path("volume.png"), icon_size=(21, 21),
            role="secondary",
        )
        bottom_layout.addWidget(self.btn_mute)

        # La barra inferior NO pertenece al layout vertical del contenido.
        # Su fila propia la mantiene anclada al borde inferior en ambos estados.
        self.bottom_host = QWidget()
        bottom_host_layout = QHBoxLayout(self.bottom_host)
        bottom_host_layout.setContentsMargins(28, 0, 28, 14)
        bottom_host_layout.setSpacing(0)
        bottom_host_layout.addWidget(self.bottom)

        main_layout.addWidget(self.bottom_host, 1, 1)

        self._inicializar_audio()

    def _abrir_kofi(self):
        dialog = KofiModal(self)
        dialog.exec()

    def _abrir_settings(self):
        dialog = SettingsModal(self)
        dialog.exec()

    # ------------------------------------------------------------------
    # TIENDAS
    # ------------------------------------------------------------------

    def _crear_burbujas_tiendas(self):
        icon_map = {
            "Epic Games": "epic.png",
            "Steam": "steam.png",
            "GOG": "gog.png",
            "Amazon Prime": "amazon_prime.png",
            "Itch.io": "itch_io.png",
            "Humble Store": "humble_store.png",
            "Fanatical": "fanatical.png",
            "IndieGala": "indiegala.png",
            "Otras Plataformas": "other.png",
        }
        for idx, store in enumerate(STORES_MAPPING.values()):
            widget = StoreWidget(self, store, icon_map.get(store, "other.png"))
            self.store_layout.addWidget(widget, 0, idx)
            self.bubble_widgets[store] = widget
            self.acordeon_estados.setdefault(store, True)

    def _on_bubble_hover(self, store, is_hover):
        widget = self.bubble_widgets.get(store)
        if widget is None:
            return
        if is_hover:
            widget.setProperty("hovering", True)
        else:
            widget.setProperty("hovering", False)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _sync_store_states(self):
        for store, widget in self.bubble_widgets.items():
            widget.setProperty("active", bool(self.active_filters.get(store, False)))
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    # ------------------------------------------------------------------
    # AUDIO
    # ------------------------------------------------------------------

    def _inicializar_audio(self):
        """Conserva la música iniciada por main.py y evita reinicios/cortes."""
        try:
            if not os.path.exists(AUDIO_PATH):
                return

            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=44100,
                    size=-16,
                    channels=2,
                    buffer=512,
                )

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.abspath(AUDIO_PATH))
                pygame.mixer.music.set_volume(0.05)
                pygame.mixer.music.play(-1)

            self.audio_silenciado = False
            self.volumen_anterior = 20
            volumen_actual = int(round(pygame.mixer.music.get_volume() * 100))
            if volumen_actual <= 0:
                volumen_actual = 5
                pygame.mixer.music.set_volume(volumen_actual / 100.0)
            self.slider_volumen.blockSignals(True)
            self.slider_volumen.setValue(volumen_actual)
            self.slider_volumen.blockSignals(False)

        except Exception as e:
            print(f"⚠️ No se pudo inicializar el audio: {e}")

    def _fade_audio(self, porcentaje):
        try:
            porcentaje = max(0, min(20, porcentaje))
            pygame.mixer.music.set_volume(porcentaje / 100.0)
            self.slider_volumen.blockSignals(True)
            self.slider_volumen.setValue(porcentaje)
            self.slider_volumen.blockSignals(False)
            if porcentaje < 20:
                QTimer.singleShot(100, lambda: self._fade_audio(porcentaje + 1))
        except Exception:
            pass

    def cambiar_volumen(self, valor):
        try:
            if self.btn_mute is None:
                return
            porcentaje = max(0, min(100, int(float(valor))))
            pygame.mixer.music.set_volume(porcentaje / 100.0)
            if porcentaje > 0:
                self.audio_silenciado = False
                self.volumen_anterior = porcentaje
                self.btn_mute.set_icon(self._icon_path("volume.png"))
            else:
                self.audio_silenciado = True
                self.btn_mute.set_icon(self._icon_path("mute.png"))
        except Exception as e:
            print(f"⚠️ Error cambiando volumen: {e}")

    def alternar_mute(self):
        try:
            if not self.audio_silenciado:
                self.volumen_anterior = int(self.slider_volumen.value())
                pygame.mixer.music.set_volume(0.0)
                self.slider_volumen.setValue(0)
                self.audio_silenciado = True
                self.btn_mute.set_icon(self._icon_path("mute.png"))
            else:
                vol = self.volumen_anterior if self.volumen_anterior > 0 else 10
                pygame.mixer.music.set_volume(vol / 100.0)
                self.slider_volumen.setValue(vol)
                self.audio_silenciado = False
                self.btn_mute.set_icon(self._icon_path("volume.png"))
        except Exception as e:
            print(f"⚠️ Error alternando mute: {e}")

    def _detener_audio(self):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # DATOS / API
    # ------------------------------------------------------------------

    def _set_status(self, text, status="success"):
        self.status_pill.setText(text)
        colores = {
            "success": COLOR_SUCCESS,
            "warning": COLOR_WARNING,
            "error": COLOR_ERROR,
            "accent": COLOR_ACCENT_LIGHT,
        }
        self.status_pill.set_colors(
            bg=COLOR_BG_CARD,
            hover=COLOR_HOVER,
            fg=colores.get(status, COLOR_SUCCESS),
            border=COLOR_BORDER,
        )

    def buscar_juegos(self):
        limpiar_cache_imagenes()
        self._set_status("● BUSCANDO", "warning")
        QApplication.processEvents()
        try:
            response = requests.get(API_URL, headers=API_HEADERS, timeout=10)
            response.raise_for_status()
            giveaways = response.json()
            if not isinstance(giveaways, list):
                raise ValueError("Formato de API no válido")

            juegos_validos = []
            exclusiones_totales = list(EXCLUSIONES) + [
                "dlc", "demo", "soundtrack", "ost", "expansion",
                "pack", "bundle", "skin", "avatar",
            ]

            for g in giveaways:
                titulo = str(g.get("title", "")).lower()
                g_type = str(g.get("type", "")).lower()
                if any(exc in g_type for exc in ["dlc", "loot", "demo", "soundtrack"]):
                    continue
                if any(exc in titulo for exc in exclusiones_totales):
                    continue
                juegos_validos.append(g)

            juegos_unicos = {}
            for juego in juegos_validos:
                clave = self._clave_juego(juego)
                if clave not in juegos_unicos:
                    juegos_unicos[clave] = juego

            self.juegos_cache_global = list(juegos_unicos.values())

            historico_actualizado = False
            for juego in self.juegos_cache_global:
                clave = self._clave_juego(juego)
                registro = self.reclamados.get(clave)
                if registro is not None:
                    valor_actual = self._valor_juego(juego)
                    if valor_actual > 0 and self._parsear_valor_juego(registro.get("worth_value")) <= 0:
                        registro["worth_value"] = valor_actual
                        registro["worth"] = str(juego.get("worth") or "")
                        historico_actualizado = True
            if historico_actualizado:
                self._guardar_reclamados()
            self._actualizar_contador_ahorrado()

            disponibles = [j for j in self.juegos_cache_global if not self._esta_reclamado(j)]
            conteos = {s: 0 for s in STORES_MAPPING.values()}
            for juego in disponibles:
                tienda = self._asignar_tienda(juego)
                if tienda in conteos:
                    conteos[tienda] += 1

            self.actualizar_insignias(conteos)
            self._set_status(f"● {len(disponibles)} OFERTAS", "success")
            self.btn_side_todas.show()
            self.mostrando_reclamados = False
            self._actualizar_visibilidad_atras()
            self._actualizar_vista_juegos()

        except Exception as e:
            self._set_status("● ERROR", "error")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los juegos:\n{e}")

    def _asignar_tienda(self, juego):
        platforms = str(juego.get("platforms", "")).lower()
        store_field = str(juego.get("store", "")).lower()
        title = str(juego.get("title", "")).lower()
        url = str(juego.get("open_giveaway_url", "")).lower()
        t = f"{platforms} {store_field} {title} {url}"

        if any(k in t for k in ["prime gaming", "amazon", "twitch", "luna"]):
            return "Amazon Prime"
        if any(k in t for k in ["gog", "gog.com"]):
            return "GOG"
        if any(k in t for k in ["humble", "humblebundle"]):
            return "Humble Store"
        if any(k in t for k in ["fanatical", "bundlestars"]):
            return "Fanatical"
        if any(k in t for k in ["epic", "epicgames"]):
            return "Epic Games"
        if "steam" in t:
            return "Steam"
        if any(k in t for k in ["itch", "itch.io"]):
            return "Itch.io"
        if "indiegala" in t:
            return "IndieGala"
        return "Otras Plataformas"

    def actualizar_insignias(self, conteos):
        for store, count in conteos.items():
            widget = self.bubble_widgets.get(store)
            if widget is None:
                continue
            widget.set_count(count)
            widget.setProperty("count", int(count))
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    # ------------------------------------------------------------------
    # VISTA
    # ------------------------------------------------------------------

    def _clear_layout(self, layout):
        """Retira widgets de un layout sin reconstruir el árbol principal ni reconstruir la ventana."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

    def _actualizar_visibilidad_contenedor_juegos(self):
        """Contrae la zona de juegos vacía y la muestra solo cuando hay contenido."""
        hay_tiendas_activas = any(self.active_filters.values())
        hay_contenido = bool(
            self.mostrando_reclamados
            or (self.juegos_cache_global and hay_tiendas_activas)
        )
        if self.container.isVisible() != hay_contenido:
            self.container.setVisible(hay_contenido)

    def _actualizar_vista_juegos(self):
        # Qt sustituye los hijos de la zona de contenido mediante deleteLater().
        # El QMainWindow y su árbol estructural permanecen intactos.
        self._clear_layout(self.frame_lista_layout)
        self._actualizar_visibilidad_contenedor_juegos()

        if self.mostrando_reclamados:
            self._mostrar_lista_reclamados()
            return

        tiendas = [s for s, a in self.active_filters.items() if a]
        if not tiendas:
            return

        for store in tiendas:
            juegos = [
                j for j in self.juegos_cache_global
                if self._asignar_tienda(j) == store and not self._esta_reclamado(j)
            ]
            open_ = self.acordeon_estados.get(store, True)

            header = QFrame()
            header.setObjectName("storeHeader")
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(0)

            arrow = "▼" if open_ else "▶"
            header_button = QPushButton(f"{arrow}   {store.upper()}")
            header_button.setObjectName("storeHeaderButton")
            header_button.clicked.connect(lambda checked=False, s=store: self._toggle_acordeon(s))
            header_layout.addWidget(header_button)

            count_label = QLabel(f"{len(juegos)} ofertas")
            count_label.setObjectName("offerCount")
            header_layout.addWidget(count_label)
            self.frame_lista_layout.addWidget(header)

            if not open_:
                continue

            if not juegos:
                empty = QLabel(f"No hay elementos disponibles en {store} actualmente.")
                empty.setObjectName("emptyLabel")
                empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
                empty.setMinimumHeight(30)
                self.frame_lista_layout.addWidget(empty)
                continue

            for juego in juegos:
                self.frame_lista_layout.addWidget(GameCard(self, juego, store))

        self.frame_lista_layout.addStretch(1)

    def _toggle_acordeon(self, store):
        self.acordeon_estados[store] = not self.acordeon_estados.get(store, True)
        self._actualizar_vista_juegos()

    # ------------------------------------------------------------------
    # HISTÓRICO
    # ------------------------------------------------------------------

    def _ruta_reclamados(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "reclamados.json")

    def _cargar_reclamados(self):
        ruta = self._ruta_reclamados()
        try:
            if not os.path.exists(ruta):
                return {}
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            if not isinstance(datos, dict):
                return {}

            limpios = {}
            for registro in datos.values():
                if not isinstance(registro, dict):
                    continue
                titulo = " ".join(str(registro.get("title") or "").lower().split()).strip()
                tienda = " ".join(str(registro.get("store") or "Otras Plataformas").lower().split()).strip()
                for sufijo in (" giveaway", " - giveaway"):
                    if titulo.endswith(sufijo):
                        titulo = titulo[:-len(sufijo)].strip()
                clave = f"game:{tienda}|{titulo}"

                if clave not in limpios:
                    registro_limpio = dict(registro)
                    if "worth_value" not in registro_limpio:
                        registro_limpio["worth_value"] = self._parsear_valor_juego(registro_limpio.get("worth"))
                    registro_limpio["key"] = clave
                    limpios[clave] = registro_limpio
                else:
                    anterior = limpios[clave]
                    if str(registro.get("claimed_at", "")) > str(anterior.get("claimed_at", "")):
                        registro_limpio = dict(registro)
                        if "worth_value" not in registro_limpio:
                            registro_limpio["worth_value"] = self._parsear_valor_juego(registro_limpio.get("worth"))
                        registro_limpio["key"] = clave
                        limpios[clave] = registro_limpio

            if limpios != datos:
                try:
                    with open(ruta, "w", encoding="utf-8") as f:
                        json.dump(limpios, f, ensure_ascii=False, indent=2)
                except Exception:
                    pass
            return limpios
        except Exception:
            return {}

    def _parsear_valor_juego(self, valor):
        if valor is None:
            return 0.0
        if isinstance(valor, (int, float)):
            return max(0.0, float(valor))
        texto = str(valor).strip()
        if not texto or texto.upper() in {"N/A", "NA", "NONE", "NULL", "FREE"}:
            return 0.0
        limpio = re.sub(r"[^0-9,.-]", "", texto)
        if not limpio:
            return 0.0
        if "," in limpio and "." in limpio:
            if limpio.rfind(",") > limpio.rfind("."):
                limpio = limpio.replace(".", "").replace(",", ".")
            else:
                limpio = limpio.replace(",", "")
        elif "," in limpio:
            partes = limpio.split(",")
            if len(partes[-1]) in (1, 2):
                limpio = "".join(partes[:-1]) + "." + partes[-1]
            else:
                limpio = limpio.replace(",", "")
        try:
            return max(0.0, float(limpio))
        except (TypeError, ValueError):
            return 0.0

    def _valor_juego(self, juego):
        if not isinstance(juego, dict):
            return 0.0
        return self._parsear_valor_juego(juego.get("worth_value", juego.get("worth")))

    def _dinero_ahorrado(self):
        total = 0.0
        for registro in self.reclamados.values():
            if isinstance(registro, dict):
                total += self._parsear_valor_juego(
                    registro.get("worth_value", registro.get("worth"))
                )
        return total

    def _actualizar_contador_ahorrado(self):
        if not hasattr(self, "ahorro_pill"):
            return
        total = self._dinero_ahorrado()
        self.ahorro_pill.setText(f"$ AHORRADO : {total:,.2f}")

    def _guardar_reclamados(self):
        try:
            with open(self._ruta_reclamados(), "w", encoding="utf-8") as f:
                json.dump(self.reclamados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"No se pudo guardar el histórico de reclamados:\n{e}")

    def _clave_juego(self, juego):
        titulo = " ".join(str(juego.get("title") or "").lower().split()).strip()
        tienda = " ".join(str(self._asignar_tienda(juego) or "").lower().split()).strip()
        for sufijo in (" giveaway", " - giveaway"):
            if titulo.endswith(sufijo):
                titulo = titulo[:-len(sufijo)].strip()
        return f"game:{tienda}|{titulo}"

    def _esta_reclamado(self, juego):
        clave_guardada = juego.get("__reclamado_key")
        if clave_guardada:
            return clave_guardada in self.reclamados
        return self._clave_juego(juego) in self.reclamados

    def _abrir_reclamacion(self, url):
        if url:
            webbrowser.open(url)

    def _alternar_reclamado(self, juego):
        clave = self._clave_juego(juego)
        if clave in self.reclamados:
            del self.reclamados[clave]
        else:
            self.reclamados[clave] = {
                "key": clave,
                "id": juego.get("id"),
                "title": str(juego.get("title") or "Elemento sin título"),
                "store": self._asignar_tienda(juego),
                "image": juego.get("image") or juego.get("thumbnail"),
                "description": juego.get("description") or "",
                "open_giveaway_url": str(juego.get("open_giveaway_url") or ""),
                "worth": str(juego.get("worth") or ""),
                "worth_value": self._valor_juego(juego),
                "worth_currency": "USD",
                "claimed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        self._guardar_reclamados()
        self._actualizar_contador_ahorrado()
        self._actualizar_vista_juegos()

        disponibles = [j for j in self.juegos_cache_global if not self._esta_reclamado(j)]
        conteos = {s: 0 for s in STORES_MAPPING.values()}
        for j in disponibles:
            tienda = self._asignar_tienda(j)
            if tienda in conteos:
                conteos[tienda] += 1
        self.actualizar_insignias(conteos)

        if self.mostrando_reclamados:
            self._set_status(f"● {len(self.reclamados)} RECLAMADOS", "accent")
        else:
            self._set_status(f"● {len(disponibles)} OFERTAS", "success")

    def mostrar_reclamados(self):
        self.mostrando_reclamados = not self.mostrando_reclamados
        if self.mostrando_reclamados:
            self.btn_reclamados.setText("★ VER RECLAMADOS")
            self.btn_reclamados.setProperty("role", "accent")
            self._set_status(f"● {len(self.reclamados)} RECLAMADOS", "accent")
        else:
            self.btn_reclamados.setText("★ RECLAMADOS")
            self.btn_reclamados.setProperty("role", "secondary")
            disponibles = [j for j in self.juegos_cache_global if not self._esta_reclamado(j)]
            self._set_status(f"● {len(disponibles)} OFERTAS", "success")
        self.btn_reclamados.style().unpolish(self.btn_reclamados)
        self.btn_reclamados.style().polish(self.btn_reclamados)
        self._actualizar_visibilidad_atras()
        self._actualizar_vista_juegos()

    def _mostrar_lista_reclamados(self):
        if not self.reclamados:
            label = QLabel("AÚN NO TIENES JUEGOS RECLAMADOS")
            label.setObjectName("emptyLabel")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setMinimumHeight(80)
            self.frame_lista_layout.addWidget(label)
            self.frame_lista_layout.addStretch(1)
            return

        header = QFrame()
        header.setObjectName("storeHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel(f"★  MIS RECLAMADOS  ·  {len(self.reclamados)}")
        title.setObjectName("gameTitle")
        title.setContentsMargins(14, 10, 14, 10)
        header_layout.addWidget(title)
        self.frame_lista_layout.addWidget(header)

        for registro in sorted(
            self.reclamados.values(),
            key=lambda x: str(x.get("claimed_at", "")),
            reverse=True,
        ):
            juego = {
                "id": registro.get("id"),
                "title": registro.get("title", "Elemento sin título"),
                "store": registro.get("store", ""),
                "image": registro.get("image"),
                "thumbnail": registro.get("image"),
                "description": registro.get("description", ""),
                "open_giveaway_url": registro.get("open_giveaway_url", ""),
                "worth": registro.get("worth", ""),
                "worth_value": registro.get("worth_value", 0),
                "__reclamado_key": registro.get("key"),
            }
            self.frame_lista_layout.addWidget(GameCard(self, juego, registro.get("store", "Otras Plataformas")))
        self.frame_lista_layout.addStretch(1)

    # ------------------------------------------------------------------
    # INTERACCIÓN / NAVEGACIÓN
    # ------------------------------------------------------------------

    def _crear_icono_seleccion(self, seleccionar_todas):
        """Crea un icono compacto para seleccionar o deseleccionar todas."""
        pixmap = QPixmap(28, 28)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        if seleccionar_todas:
            color = QColor(COLOR_ACCENT_LIGHT)
            marcar = True
        else:
            color = QColor(COLOR_ERROR)
            marcar = False

        pen = QPen(color, 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for y in (5, 13, 21):
            painter.drawRect(3, y - 2, 6, 6)
            painter.drawLine(12, y + 1, 24, y + 1)
            if marcar:
                painter.drawLine(4, y + 1, 6, y + 3)
                painter.drawLine(6, y + 3, 9, y - 1)
            else:
                painter.drawLine(14, y - 2, 19, y + 3)
                painter.drawLine(19, y - 2, 14, y + 3)

        painter.end()
        return QIcon(pixmap)

    def _ajustar_ventana_por_estado(self, expandida):
        """Mantiene la cabecera fija y expande solo la zona de juegos."""
        content_layout = self.content.layout()

        if expandida:
            self.setMinimumSize(980, 620)
            self.resize(max(self.width(), 1120), 720)
            self.container.show()
            self.content.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            # El panel de juegos es el unico que recibe el espacio sobrante.
            content_layout.setStretch(4, 1)
        else:
            self.setMinimumSize(980, 360)
            self.resize(max(self.width(), 1120), 360)
            # En modo compacto, el contenido tiene solo su altura natural:
            # tiendas y boton quedan arriba y no se desplazan al cambiar la
            # altura de la ventana.
            content_layout.setStretch(4, 0)
            self.container.hide()
            self.content.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

        self._centrar()

    def _actualizar_visibilidad_atras(self):
        """Muestra Atrás solo cuando existe un estado que realmente se puede deshacer."""
        hay_filtros = any(self.active_filters.values())
        hay_todas = bool(self.todas_activado)
        hay_reclamados = bool(self.mostrando_reclamados)
        hay_resultados = bool(self.juegos_cache_global)
        hay_estado = hay_filtros or hay_todas or hay_reclamados or hay_resultados

        # Cuando existe cualquier estado generado por la aplicación, las dos
        # acciones contextuales forman un bloque único justo debajo del logo.
        # Al arrancar, ambas permanecen ocultas.
        self.btn_side_todas.setVisible(hay_estado)
        self.btn_side_back.setVisible(hay_estado)

        self._ajustar_ventana_por_estado(hay_estado)

    def toggle_todas(self):
        if self.todas_activado:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.todas_activado = False
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
            self.btn_side_todas.setToolTip("Seleccionar todas")
        else:
            for s in self.active_filters:
                self.active_filters[s] = True
                self.acordeon_estados[s] = True
            self.todas_activado = True
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(False))
            self.btn_side_todas.setToolTip("Deseleccionar todas")
        self._sync_store_states()
        self._actualizar_visibilidad_atras()
        self._actualizar_vista_juegos()

    def _toggle_tienda(self, store):
        if self.todas_activado:
            self.todas_activado = False
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
            self.btn_side_todas.setToolTip("Seleccionar todas")

        if self.active_filters[store]:
            self.active_filters[store] = False
            if store in self.acordeon_estados:
                self.acordeon_estados[store] = False
        else:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.active_filters[store] = True
            self.acordeon_estados[store] = True

        self._sync_store_states()
        self._actualizar_visibilidad_atras()
        self._actualizar_vista_juegos()

    def volver_atras(self):
        self.mostrando_reclamados = False
        self.btn_reclamados.setText("★ RECLAMADOS")
        self.btn_reclamados.setProperty("role", "secondary")
        self.btn_reclamados.style().unpolish(self.btn_reclamados)
        self.btn_reclamados.style().polish(self.btn_reclamados)

        for s in self.active_filters:
            self.active_filters[s] = False
        self.tienda_seleccionada = None
        self.todas_activado = False
        self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
        self.btn_side_todas.setToolTip("Seleccionar todas")
        self.btn_side_todas.hide()
        self._sync_store_states()

        self.juegos_cache_global = []
        self._actualizar_visibilidad_atras()
        self._actualizar_vista_juegos()
        self._set_status("● LISTO", "success")

    def resetear_app(self):
        self.volver_atras()
        self.repaint()

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------

    def _centrar(self):
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            frame = self.frameGeometry()
            frame.moveCenter(geo.center())
            self.move(frame.topLeft())

    def _load_store_icon(self, path, logical_size=64):
        """Carga un icono de tienda a resolución física suficiente para el DPI de Qt."""
        if not os.path.exists(path):
            return None

        pixmap = QPixmap(path)
        if pixmap.isNull():
            return None

        screen = QApplication.primaryScreen()
        dpr = screen.devicePixelRatio() if screen is not None else 1.0
        dpr = max(1.0, float(dpr))
        physical_size = max(1, round(logical_size * dpr))

        scaled = pixmap.scaled(
            physical_size, physical_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        scaled.setDevicePixelRatio(dpr)
        return scaled

    def _load_thumbnail(self, url_img):
        if not url_img:
            return None

        cache_dir = "cache"
        os.makedirs(cache_dir, exist_ok=True)
        filename = os.path.join(
            cache_dir,
            f"{hashlib.sha256(url_img.encode('utf-8')).hexdigest()}.png",
        )

        try:
            if os.path.exists(filename):
                pixmap = QPixmap(filename)
                if not pixmap.isNull():
                    return pixmap

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            }
            res = requests.get(url_img, headers=headers, timeout=5)
            if res.status_code == 200:
                pixmap = QPixmap()
                if pixmap.loadFromData(res.content):
                    pixmap.save(filename, "PNG")
                    return pixmap
        except Exception as e:
            print(f"Error descargando miniatura ({url_img}): {e}")
        return None

    def _resize_canvas_content(self, event):
        # Compatibilidad nominal con el nombre antiguo.
        if self.frame_lista is not None:
            self.frame_lista.setMinimumWidth(max(1, event.size().width()))

    def _mousewheel(self, event):
        # Compatibilidad nominal con el nombre antiguo.
        return None

    def abrir_enlace(self, url):
        if url:
            webbrowser.open(url)

    def _apply_theme(self, bg, card, desc, text, secondary, icon_path):
        # Compatibilidad con llamadas antiguas: el tema real se obtiene
        # exclusivamente de config.THEMES.
        self.alternar_tema()

    def _icons_root(self):
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "icons",
        )

    def _icon_path(self, filename):
        return os.path.join(self._icons_root(), "navigation_ui", filename)

    def _action_icon_path(self, filename):
        return os.path.join(self._icons_root(), "actions", filename)

    def _store_icon_path(self, filename):
        return os.path.join(self._icons_root(), "stores", filename)

    # ------------------------------------------------------------------
    # CIERRE / COMPATIBILIDAD
    # ------------------------------------------------------------------

    def _cerrar_ventana(self):
        self.close()

    def closeEvent(self, event):
        try:
            self._detener_audio()
            limpiar_cache_imagenes()
        except Exception:
            pass
        if callable(self.al_cerrar_app):
            try:
                self.al_cerrar_app()
            except Exception:
                pass
        event.accept()

    def mostrar(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self._centrar()

    def run(self):
        """Compatibilidad con main.py antiguo; QApplication debe existir fuera."""
        self.show()
        self.raise_()
        self.activateWindow()


if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())
