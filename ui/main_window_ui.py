"""Construcción de la interfaz principal."""

import config

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget,
)
from config import (
    LOGO_PATH, STORES_MAPPING, COLOR_SIDEBAR, COLOR_ACCENT, COLOR_TEXT_PRIMARY,
    COLOR_BORDER, COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_BG_CARD, COLOR_HOVER,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_TEXT_MUTED,
)
from ui.game_card import RoundedButton, VolumeSlider
from ui.store_widget import StoreWidget
from ui.kofi_modal import KofiModal
from ui.settings_modal import SettingsModal


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



def instalar_metodos(cls):

    cls._build_ui = _build_ui

    cls._abrir_kofi = _abrir_kofi

    cls._abrir_settings = _abrir_settings

    cls._crear_burbujas_tiendas = _crear_burbujas_tiendas

    cls._on_bubble_hover = _on_bubble_hover

    cls._sync_store_states = _sync_store_states
