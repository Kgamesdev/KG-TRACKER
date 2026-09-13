"""Búsqueda, filtrado y construcción de la vista de juegos con validación temporal estricta a 0.00 EUR."""

import os
import json
import time
import datetime
import concurrent.futures
from PySide6.QtWidgets import (
    QApplication, QLabel, QFrame, QHBoxLayout, QPushButton,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QTimer, QObject, Signal, QThread
from config import (
    API_URL, API_HEADERS, EXCLUSIONES, STORES_MAPPING,
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_ACCENT_LIGHT,
    COLOR_TEXT_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR,
    BASE_DIR,
)
from core.images import limpiar_cache_imagenes
from ui.components.game_card import GameCard
from core.i18n import t
from logger import log_info, log_warning, log_error
from core.scrapers.store_scrapers import (
    guardar_en_cache_disco as _guardar_en_cache_disco,
    cargar_cache_otras_tiendas as _cargar_cache_otras_tiendas,
    obtener_epic_directo as _obtener_epic_directo,
    obtener_steam_directo as _obtener_steam_directo,
    obtener_itch_directo as _obtener_itch_directo,
    obtener_gog_directo as _obtener_gog_directo,
)

CACHE_GIVEAWAYS_FILE = os.path.join(BASE_DIR, "data", "giveaways_cache.json")


def _limpiar_hilo_busqueda(self):
    if hasattr(self, "_busqueda_thread") and self._busqueda_thread:
        if self._busqueda_thread.isRunning():
            self._busqueda_thread.quit()
            self._busqueda_thread.wait(500)
        self._busqueda_thread = None
    self._busqueda_worker = None


class _BusquedaWorker(QObject):
    terminado = Signal(object, str)
    error = Signal(str)

    def run(self):
        import requests
        # 1. Ruta Primaria (GamerPower) con timeout ultra-ágil de 1.2s (Constitución II)
        try:
            response = requests.get(API_URL, headers=API_HEADERS, timeout=1.2)
            response.raise_for_status()
            giveaways = response.json()
            if isinstance(giveaways, list) and len(giveaways) > 0:
                _guardar_en_cache_disco(giveaways)
                self.terminado.emit(giveaways, "gamerpower")
                return  # Cierre atómico: impidiendo la activación de la Ruta 2
        except Exception as e:
            log_warning(f"GamerPower inaccesible o timeout 1.2s ({e}).")
            log_info("Activando motor autónomo de tiendas directas...")

        # 2. Ruta Autónoma: Concurrencia multitienda (Epic, Itch.io, GOG, Steam)
        try:
            juegos_hibridos = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                f_epic = executor.submit(_obtener_epic_directo)
                f_itch = executor.submit(_obtener_itch_directo)
                f_gog = executor.submit(_obtener_gog_directo)
                f_steam = executor.submit(_obtener_steam_directo)

                for f in (f_epic, f_itch, f_gog, f_steam):
                    try:
                        res = f.result(timeout=6.0)
                        if res:
                            juegos_hibridos.extend(res)
                    except Exception as err_f:
                        log_warning(f"Error en subfuente directa: {err_f}")

            tiendas_vivas = ("Epic Games", "Itch.io", "GOG", "Steam")
            juegos_otras_tiendas = _cargar_cache_otras_tiendas(excluir_tiendas=tiendas_vivas)
            if juegos_otras_tiendas:
                juegos_hibridos.extend(juegos_otras_tiendas)

            if juegos_hibridos:
                log_info(f"Motor híbrido completado: {len(juegos_hibridos)} juegos confirmados.")
                self.terminado.emit(juegos_hibridos, "hibrido")
                return
        except Exception as err_hibrido:
            log_error(f"Error en motor autónomo: {err_hibrido}")

        self.error.emit("No se encontraron ofertas gratuitas activas en este momento.")


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
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is None:
        timer = QTimer(self)
        timer.setInterval(35)
        timer.timeout.connect(self._actualizar_animacion_busqueda)
        self._busqueda_neon_timer = timer

    self._busqueda_neon_inicio = time.monotonic()
    self._busqueda_neon_activo = True
    self.status_pill.setGraphicsEffect(None)
    self.status_pill.set_colors(bg=COLOR_BG_CARD, border=COLOR_BORDER, fg="transparent")
    timer.start()
    self._actualizar_animacion_busqueda()


def _actualizar_animacion_busqueda(self):
    if not getattr(self, "_busqueda_neon_activo", False):
        return
    import math
    from PySide6.QtGui import QColor
    fase = (time.monotonic() - getattr(self, "_busqueda_neon_inicio", time.monotonic())) * 6.0
    pulso = (1.0 + math.sin(fase)) / 2.0
    alpha = int(40 + pulso * 160)
    c = QColor("#00F3FF")
    c.setAlpha(alpha)
    self.status_pill.set_colors(
        bg=COLOR_BG_CARD,
        border=c.name(QColor.NameFormat.HexArgb),
        fg="transparent",
    )


def _detener_animacion_busqueda(self):
    self._busqueda_neon_activo = False
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is not None:
        timer.stop()
    self.status_pill.set_colors(bg=COLOR_BG_CARD, border=COLOR_BORDER, fg=COLOR_SUCCESS)
    self.status_pill.setText("LISTO")


def _finalizar_busqueda(self, giveaways, inicio, fuente="gamerpower"):
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
        urls_vistas = set()
        for juego in juegos_validos:
            clave = self._clave_juego(juego)
            url_canonica = str(juego.get("open_giveaway_url") or "").strip().rstrip("/").lower()
            if url_canonica and url_canonica in urls_vistas:
                continue
            if clave not in juegos_unicos:
                juegos_unicos[clave] = juego
                if url_canonica:
                    urls_vistas.add(url_canonica)

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
        self.mostrando_reclamados = False

        transcurrido = int((time.monotonic() - inicio) * 1000)
        espera = max(0, 1200 - transcurrido)
        espera_juegos = max(0, 1000 - transcurrido)

        def mostrar_juegos():
            self._actualizar_visibilidad_atras()
            self._actualizar_vista_juegos()

        def finalizar_estado():
            self._detener_animacion_busqueda()
            self._set_status(t("status.offers", count=len(disponibles)), "success")
            self._busqueda_en_curso = False
            self._busqueda_thread = None
            self._busqueda_worker = None

        QTimer.singleShot(espera_juegos, mostrar_juegos)
        QTimer.singleShot(espera, finalizar_estado)

    except Exception as e:
        self._detener_animacion_busqueda()
        self._busqueda_en_curso = False
        log_error(f"Error procesando lista de juegos: {e}")
        self._set_status("● ERROR", "error")


def _recibir_resultados_busqueda(self, giveaways, fuente):
    self._finalizar_busqueda(
        giveaways,
        getattr(self, "_busqueda_inicio", time.monotonic()),
        fuente=fuente,
    )


def _buscar_juegos_error(self, mensaje):
    self._detener_animacion_busqueda()
    self._busqueda_en_curso = False
    self._set_status("● SIN OFERTAS", "warning")
    log_warning(f"Aviso de búsqueda: {mensaje}")


def buscar_juegos(self):
    if getattr(self, "_busqueda_en_curso", False):
        return

    self._limpiar_hilo_busqueda()
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
    
    # Destrucción limpia y silenciosa del ciclo de vida del hilo (Constitución II)
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
    t_str = f"{platforms} {store_field} {title} {url}"

    if any(k in t_str for k in ["prime gaming", "amazon", "twitch", "luna"]):
        return "Amazon Prime"
    if any(k in t_str for k in ["gog", "gog.com"]):
        return "GOG"
    if any(k in t_str for k in ["humble", "humblebundle"]):
        return "Humble Store"
    if any(k in t_str for k in ["fanatical", "bundlestars"]):
        return "Fanatical"
    if any(k in t_str for k in ["epic", "epicgames"]):
        return "Epic Games"
    if "steam" in t_str:
        return "Steam"
    if any(k in t_str for k in ["itch", "itch.io"]):
        return "Itch.io"
    if "indiegala" in t_str:
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
    pass


def _actualizar_visibilidad_contenedor_juegos(self):
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
        self._actualizar_visibilidad_contenedor_juegos()

        juegos_visibles_ordenados = []
        juegos_a_mostrar_map = {}

        if getattr(self, "mostrando_reclamados", False):
            lista_reclamados = sorted(self.reclamados.values(), key=lambda j: j.get('title', ''))
            for juego in lista_reclamados:
                clave = self._clave_juego(juego)
                juegos_visibles_ordenados.append(clave)
                juegos_a_mostrar_map[clave] = {'juego': juego, 'tienda': "Reclamados"}
        else:
            tiendas_activas = {s for s, a in self.active_filters.items() if a}
            juegos_filtrados = [
                j for j in self.juegos_cache_global
                if self._asignar_tienda(j) in tiendas_activas and not self._esta_reclamado(j)
            ]
            juegos_por_tienda = {}
            for juego in juegos_filtrados:
                tienda = self._asignar_tienda(juego)
                if tienda not in juegos_por_tienda:
                    juegos_por_tienda[tienda] = []
                juegos_por_tienda[tienda].append(juego)

            for tienda in sorted(juegos_por_tienda.keys()):
                clave_header = f"header_{tienda}"
                juegos_visibles_ordenados.append(clave_header)
                juegos_a_mostrar_map[clave_header] = {'tienda': tienda, 'juegos_count': len(juegos_por_tienda[tienda])}

                if self.acordeon_estados.get(tienda, True):
                    for juego in sorted(juegos_por_tienda[tienda], key=lambda j: j.get('title', '')):
                        clave = self._clave_juego(juego)
                        juegos_visibles_ordenados.append(clave)
                        juegos_a_mostrar_map[clave] = {'juego': juego, 'tienda': tienda}

        widgets_actuales = set(self.game_widgets_map.keys())
        widgets_necesarios = set(juegos_visibles_ordenados)

        for clave in widgets_actuales - widgets_necesarios:
            widget = self.game_widgets_map.pop(clave)
            widget.setParent(None)
            widget.deleteLater()

        for i, clave in enumerate(juegos_visibles_ordenados):
            if clave not in self.game_widgets_map:
                data = juegos_a_mostrar_map[clave]
                if clave.startswith("header_"):
                    tienda = data['tienda']
                    open_ = self.acordeon_estados.get(tienda, True)
                    header = QFrame()
                    header.setObjectName("storeHeader")
                    header_layout = QHBoxLayout(header)
                    header_layout.setContentsMargins(0, 0, 0, 0)
                    header_layout.setSpacing(0)
                    arrow = "▼" if open_ else "▶"
                    header_button = QPushButton(f"{arrow}  {tienda.upper()}")
                    header_button.setObjectName("storeHeaderButton")
                    header_button.clicked.connect(lambda checked=False, s=tienda: self._toggle_acordeon(s))
                    header_layout.addWidget(header_button)
                    count_label = QLabel(f"{data['juegos_count']} ofertas")
                    count_label.setObjectName("offerCount")
                    header_layout.addWidget(count_label)
                    widget = header
                else:
                    widget = GameCard(self, data['juego'], data['tienda'])
                self.game_widgets_map[clave] = widget

            widget = self.game_widgets_map[clave]
            self.frame_lista_layout.insertWidget(i, widget)
        
        while self.frame_lista_layout.count() > len(juegos_visibles_ordenados):
            item = self.frame_lista_layout.takeAt(len(juegos_visibles_ordenados))
            if item.widget():
                item.widget().deleteLater()

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
    cls.game_widgets_map = {}
    cls._limpiar_hilo_busqueda = _limpiar_hilo_busqueda
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
