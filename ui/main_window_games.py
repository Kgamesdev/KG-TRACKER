import config
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
from ui.components.game_card import GameCard, StoreHeaderBanner
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
        try:
            response = requests.get(API_URL, headers=API_HEADERS, timeout=5.0)
            response.raise_for_status()
            giveaways = response.json()
            if isinstance(giveaways, list) and len(giveaways) > 0:
                _guardar_en_cache_disco(giveaways)
                self.terminado.emit(giveaways, "gamerpower")
                return
        except Exception as e:
            log_warning(f"GamerPower inaccesible o timeout 1.2s ({e}).")
            log_info("Activando motor autónomo de tiendas directas...")

        try:
            juegos_hibridos = []

            def _ejecutar_scraper_con_sesion(fn):
                with requests.Session() as s:
                    return fn(session=s)

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                f_epic = executor.submit(_ejecutar_scraper_con_sesion, _obtener_epic_directo)
                f_itch = executor.submit(_ejecutar_scraper_con_sesion, _obtener_itch_directo)
                f_gog = executor.submit(_ejecutar_scraper_con_sesion, _obtener_gog_directo)
                f_steam = executor.submit(_ejecutar_scraper_con_sesion, _obtener_steam_directo)

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
    es_oscuro = getattr(self, "es_modo_oscuro", config.CURRENT_THEME == "dark")
    if not es_oscuro:
        if status == "success":
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10B981, stop:1 #34D399); color: #FFFFFF; border: 1.2px solid #6EE7B7; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        elif status == "warning":
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F59E0B, stop:1 #D97706); color: #FFFFFF; border: 1.2px solid #FCD34D; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        elif status == "error":
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #EF4444, stop:1 #DC2626); color: #FFFFFF; border: 1.2px solid #FCA5A5; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        else:
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4F46E5, stop:1 #6366F1); color: #FFFFFF; border: 1.2px solid #818CF8; border-radius: 10px; font-weight: bold; padding: 0 10px;"
    else:
        if status == "success":
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10B981, stop:1 #059669); color: #FFFFFF; border: 1px solid #34D399; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        elif status == "warning":
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF9800, stop:1 #E65100); color: #FFFFFF; border: 1px solid #FFE082; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        elif status == "error":
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #EF4444, stop:1 #B91C1C); color: #FFFFFF; border: 1px solid #FCA5A5; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        else:
            estilo = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6366F1, stop:1 #4F46E5); color: #FFFFFF; border: 1px solid #818CF8; border-radius: 10px; font-weight: bold; padding: 0 10px;"
    self.status_pill.setStyleSheet(estilo)


def _iniciar_animacion_busqueda(self):
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is None:
        timer = QTimer(self)
        timer.setInterval(35)
        timer.timeout.connect(self._actualizar_animacion_busqueda)
        self._busqueda_neon_timer = timer

    self._busqueda_neon_inicio = time.monotonic()
    self._busqueda_neon_activo = True
    self.status_pill.setText(t("status.searching"))
    timer.start()
    self._actualizar_animacion_busqueda()


def _actualizar_animacion_busqueda(self):
    if not getattr(self, "_busqueda_neon_activo", False):
        return
    import math
    fase = (time.monotonic() - getattr(self, "_busqueda_neon_inicio", time.monotonic())) * 6.5
    pulso = (1.0 + math.sin(fase)) / 2.0
    
    color_arriba = "#FFA726" if pulso > 0.5 else "#FB8C00"
    color_abajo = "#E65100" if pulso > 0.5 else "#BF360C"
    
    estilo = f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color_arriba}, stop:1 {color_abajo}); color: #FFFFFF; border: 1.5px solid #FFE082; border-radius: 10px; font-weight: bold; padding: 0 10px;"
    self.status_pill.setStyleSheet(estilo)


def _detener_animacion_busqueda(self):
    self._busqueda_neon_activo = False
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is not None:
        timer.stop()


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
        espera_total = max(0, 2400 - transcurrido)

        def mostrar_juegos_y_estado():
            self._detener_animacion_busqueda()
            if len(disponibles) > 0:
                self._set_status(t("status.offers", count=len(disponibles)), "success")
            else:
                self._set_status(t("status.ready"), "success")
            self._actualizar_visibilidad_atras()
            self._actualizar_vista_juegos()
            self._busqueda_en_curso = False
            self._busqueda_thread = None
            self._busqueda_worker = None

        QTimer.singleShot(espera_total, mostrar_juegos_y_estado)

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
    self._set_status(t("status.error"), "error")
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
    if not hay_contenido:
        self.container.setVisible(False)
        self.container.setMaximumHeight(0)
    elif not self.container.isVisible():
        self.container.setMaximumHeight(0)
        self.container.setVisible(True)

def _actualizar_vista_juegos(self):
    from core.i18n import t
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QParallelAnimationGroup, QSequentialAnimationGroup, QPauseAnimation

    root = self.centralWidget()
    if root is not None:
        root.setUpdatesEnabled(False)
        
    try:
        self._actualizar_visibilidad_contenedor_juegos()

        juegos_visibles_ordenados = []
        juegos_a_mostrar_map = {}

        if getattr(self, "mostrando_reclamados", False):
            lista_reclamados = sorted(self.reclamados.values(), key=lambda j: j.get('title', ''))
            clave_banner = "banner_reclamados"
            juegos_visibles_ordenados.append(clave_banner)
            juegos_a_mostrar_map[clave_banner] = {
                'tipo': 'banner',
                'titulo': f"★  MIS RECLAMADOS  ·  {len(lista_reclamados)}",
            }
            for juego in lista_reclamados:
                clave = self._clave_juego(juego)
                juegos_visibles_ordenados.append(clave)
                juegos_a_mostrar_map[clave] = {'tipo': 'juego', 'juego': juego, 'tienda': "Reclamados"}
        else:
            tiendas_activas = [s for s, a in self.active_filters.items() if a]
            juegos_filtrados = [
                j for j in self.juegos_cache_global
                if self._asignar_tienda(j) in tiendas_activas and not self._esta_reclamado(j)
            ]
            
            if len(tiendas_activas) == 1:
                tienda_nombre = tiendas_activas[0]
                clave_banner = f"banner_{tienda_nombre}"
                juegos_visibles_ordenados.append(clave_banner)
                conteo_texto = t("store.offers_count", count=len(juegos_filtrados)).upper()
                juegos_a_mostrar_map[clave_banner] = {
                    'tipo': 'banner',
                    'titulo': f"{tienda_nombre.upper()}  ·  {conteo_texto}",
                }
            elif len(tiendas_activas) > 1:
                clave_banner = "banner_todas"
                juegos_visibles_ordenados.append(clave_banner)
                conteo_texto = t("store.offers_count", count=len(juegos_filtrados)).upper()
                juegos_a_mostrar_map[clave_banner] = {
                    'tipo': 'banner',
                    'titulo': f"🌐  TODAS LAS TIENDAS  ·  {conteo_texto}",
                }

            for juego in sorted(juegos_filtrados, key=lambda j: (self._asignar_tienda(j), j.get('title', ''))):
                clave = self._clave_juego(juego)
                tienda = self._asignar_tienda(juego)
                juegos_visibles_ordenados.append(clave)
                juegos_a_mostrar_map[clave] = {'tipo': 'juego', 'juego': juego, 'tienda': tienda}

        widgets_actuales = set(self.game_widgets_map.keys())
        widgets_necesarios = set(juegos_visibles_ordenados)

        for clave in widgets_actuales - widgets_necesarios:
            widget = self.game_widgets_map.pop(clave)
            self.frame_lista_layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

        while self.frame_lista_layout.count() > 0:
            last_item = self.frame_lista_layout.itemAt(self.frame_lista_layout.count() - 1)
            if last_item.spacerItem():
                self.frame_lista_layout.removeItem(last_item)
            else:
                break

        widgets_to_animate = []

        for i, clave in enumerate(juegos_visibles_ordenados):
            es_nuevo = False
            if clave not in self.game_widgets_map:
                data = juegos_a_mostrar_map[clave]
                if data.get('tipo') == 'banner':
                    from ui.components.game_card import StoreHeaderBanner
                    widget = StoreHeaderBanner(self.frame_lista, data['titulo'])
                else:
                    from ui.components.game_card import GameCard
                    widget = GameCard(self, data['juego'], data['tienda'])
                self.game_widgets_map[clave] = widget
                es_nuevo = True

            widget = self.game_widgets_map[clave]
            
            if es_nuevo:
                if hasattr(widget, "preparar_animacion_cascada"):
                    pass
                    widgets_to_animate.append(widget)
            else:
                if hasattr(widget, "graphicsEffect") and widget.graphicsEffect():
                    widget.graphicsEffect().setOpacity(1.0)
                    
            self.frame_lista_layout.insertWidget(i, widget)
            widget.show()

        self.frame_lista_layout.addStretch(1)
        self.frame_lista_layout.activate()
        QApplication.processEvents()

    finally:
        if root is not None:
            root.setUpdatesEnabled(True)

    # Animacion fluida de acordeon sincronizado
    if self.container.isVisible():
        from PySide6.QtCore import QPropertyAnimation, QEasingCurve
        target_height = min(680, max(260, len(juegos_visibles_ordenados) * 160 + 60))
        if self.container.height() < 50:
            anim_cajon = QPropertyAnimation(self.container, b"maximumHeight", self)
            anim_cajon.setDuration(300)
            anim_cajon.setStartValue(0)
            anim_cajon.setEndValue(target_height)
            anim_cajon.setEasingCurve(QEasingCurve.Type.OutCubic)

            def _restaurar_max():
                self.container.setMaximumHeight(16777215)
            anim_cajon.finished.connect(_restaurar_max)
            self._cajon_anim = anim_cajon
            anim_cajon.start()
        else:
            self.container.setMaximumHeight(16777215)

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




