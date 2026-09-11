"""Búsqueda, filtrado y construcción de la vista de juegos."""

import time
import requests
from PySide6.QtWidgets import (
    QApplication, QLabel, QFrame, QHBoxLayout, QPushButton,
    QMessageBox, QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QTimer, QObject, Signal, QThread
from PySide6.QtGui import QColor
from config import (
    API_URL, API_HEADERS, EXCLUSIONES, STORES_MAPPING,
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_ACCENT_LIGHT,
    COLOR_TEXT_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR,
)
from core.images import limpiar_cache_imagenes
from ui.game_card import GameCard


class _BusquedaWorker(QObject):
    terminado = Signal(object)
    error = Signal(str)

    def run(self):
        try:
            response = requests.get(API_URL, headers=API_HEADERS, timeout=10)
            response.raise_for_status()
            giveaways = response.json()
            if not isinstance(giveaways, list):
                raise ValueError("Formato de API no válido")
            self.terminado.emit(giveaways)
        except Exception as e:
            self.error.emit(str(e))


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


def _iniciar_animacion_busqueda(self):
    """Activa un neon suave alrededor del botón LISTO durante la búsqueda."""
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is None:
        timer = QTimer(self)
        timer.setInterval(35)
        timer.timeout.connect(self._actualizar_animacion_busqueda)
        self._busqueda_neon_timer = timer

    effect = getattr(self, "_busqueda_neon_effect", None)
    if effect is None:
        effect = QGraphicsDropShadowEffect(self.status_pill)
        effect.setOffset(0, 0)
        self.status_pill.setGraphicsEffect(effect)
        self._busqueda_neon_effect = effect

    self._busqueda_neon_inicio = time.monotonic(); self._busqueda_neon_activo = True; self.status_pill.setGraphicsEffect(None); self.status_pill.set_colors(bg=COLOR_BG_CARD, border=COLOR_BORDER, fg='transparent'); timer.start(); self._actualizar_animacion_busqueda()


def _actualizar_animacion_busqueda(self):
    if not getattr(self, "_busqueda_neon_activo", False): return
    fase = (time.monotonic() - getattr(self, "_busqueda_neon_inicio", time.monotonic())) * 6.0
    pulso = (1.0 + __import__("math").sin(fase)) / 2.0; alpha = int(40 + pulso * 160); c = __import__('PySide6.QtGui', fromlist=['QColor']).QColor('#00F3FF'); c.setAlpha(alpha)
    self.status_pill.set_colors(bg=COLOR_BG_CARD, border=c.name(__import__('PySide6.QtGui', fromlist=['QColor']).QColor.NameFormat.HexArgb), fg='transparent')


def _detener_animacion_busqueda(self):
    self._busqueda_neon_activo = False
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is not None: timer.stop()
    self.status_pill.set_colors(bg=COLOR_BG_CARD, border=COLOR_BORDER, fg=COLOR_SUCCESS); self.status_pill.setText("● LISTO")


def _finalizar_busqueda(self, giveaways, inicio):
    try:
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
        # self.btn_side_todas.show()
        self.mostrando_reclamados = False

        transcurrido = int((time.monotonic() - inicio) * 1000)
        espera = max(0, 2000 - transcurrido)
        espera_juegos = max(0, 1500 - transcurrido)

        def mostrar_juegos():
            self._actualizar_visibilidad_atras()
            self._actualizar_vista_juegos()

        def finalizar_estado():
            self._detener_animacion_busqueda()
            self._set_status(f"● {len(disponibles)} OFERTAS", "success")
            self._busqueda_en_curso = False
            self._busqueda_thread = None
            self._busqueda_worker = None

        QTimer.singleShot(espera_juegos, mostrar_juegos)
        QTimer.singleShot(espera, finalizar_estado)

    except Exception as e:
        self._detener_animacion_busqueda()
        self._busqueda_en_curso = False
        QMessageBox.critical(self, "Error", f"No se pudieron cargar los juegos:\n{e}")


def _recibir_resultados_busqueda(self, giveaways):
    self._finalizar_busqueda(
        giveaways,
        getattr(self, "_busqueda_inicio", time.monotonic())
    )


def _buscar_juegos_error(self, mensaje):
    self._detener_animacion_busqueda()
    self._busqueda_en_curso = False
    self._set_status("● ERROR", "error")
    QMessageBox.critical(self, "Error", f"No se pudieron cargar los juegos:\n{mensaje}")


def buscar_juegos(self):
    if getattr(self, "_busqueda_en_curso", False):
        return

    limpiar_cache_imagenes()
    self._busqueda_en_curso = True
    self._busqueda_inicio = time.monotonic()
    self._iniciar_animacion_busqueda()
    QApplication.processEvents()

    thread = QThread(self)
    worker = _BusquedaWorker()
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.terminado.connect(self._recibir_resultados_busqueda)
    worker.error.connect(self._buscar_juegos_error)
    worker.terminado.connect(thread.quit)
    worker.error.connect(thread.quit)
    thread.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    self._busqueda_thread = thread
    self._busqueda_worker = worker
    thread.start()


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
    root = self.centralWidget()
    if root is not None:
        root.setUpdatesEnabled(False)
    try:
        self._clear_layout(self.frame_lista_layout)
        self._actualizar_visibilidad_contenedor_juegos()

        if getattr(self, 'mostrando_reclamados', False):
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
    finally:
        if root is not None:
            root.setUpdatesEnabled(True)
            root.update()



def _toggle_acordeon(self, store):
    root = self.centralWidget()
    if root is not None:
        root.setUpdatesEnabled(False)
    try:
        self.acordeon_estados[store] = not self.acordeon_estados.get(store, True)
        self._actualizar_vista_juegos()
    finally:
        if root is not None:
            root.setUpdatesEnabled(True)
            root.update()



def instalar_metodos(cls):

    cls._set_status = _set_status

    cls._recibir_resultados_busqueda = _recibir_resultados_busqueda
    cls._buscar_juegos_error = _buscar_juegos_error
    cls.buscar_juegos = buscar_juegos
    cls._actualizar_animacion_busqueda = _actualizar_animacion_busqueda
    cls._iniciar_animacion_busqueda = _iniciar_animacion_busqueda
    cls._detener_animacion_busqueda = _detener_animacion_busqueda
    cls._finalizar_busqueda = _finalizar_busqueda

    cls._asignar_tienda = _asignar_tienda

    cls.actualizar_insignias = actualizar_insignias

    cls._clear_layout = _clear_layout

    cls._actualizar_visibilidad_contenedor_juegos = _actualizar_visibilidad_contenedor_juegos

    cls._actualizar_vista_juegos = _actualizar_vista_juegos

    cls._toggle_acordeon = _toggle_acordeon



