import config
"""Búsqueda, filtrado y construcción de la vista de juegos con validación temporal estricta a 0.00 EUR."""

import os
import json
import time
import datetime
import concurrent.futures
import re
import unicodedata
from difflib import SequenceMatcher
from urllib.parse import urlsplit, urlunsplit
from PySide6.QtWidgets import (
    QLabel, QFrame, QHBoxLayout, QPushButton,
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
    detectar_tienda_juego as _detectar_tienda_juego,
    obtener_epic_directo as _obtener_epic_directo,
    obtener_steam_directo as _obtener_steam_directo,
    obtener_itch_directo as _obtener_itch_directo,
    obtener_gog_directo as _obtener_gog_directo,
    obtener_amazon_prime_directo as _obtener_amazon_prime_directo,
    obtener_fanatical_directo as _obtener_fanatical_directo,
)

from core.paths import CACHE_GIVEAWAYS_FILE as USER_CACHE_GIVEAWAYS_FILE
CACHE_GIVEAWAYS_FILE = str(USER_CACHE_GIVEAWAYS_FILE)
_CACHE_OFERTAS_SIN_FECHA_MAX_HORAS = 12


def _clasificar_resultado_busqueda(total_fuentes, fuentes_exitosas, hay_ofertas):
    """Distingue una búsqueda vacía de otra sin ninguna fuente disponible."""
    if hay_ofertas:
        return "offers"
    if fuentes_exitosas == 0:
        return "offline"
    if fuentes_exitosas < total_fuentes:
        return "partial"
    return "empty"


def _limpiar_hilo_busqueda(self):
    thread = getattr(self, "_busqueda_thread", None)
    if thread is None:
        self._busqueda_worker = None
        return True

    try:
        if thread.isRunning():
            thread.requestInterruption()
            thread.quit()
            return False
    except RuntimeError:
        # El QThread pudo terminar y ser eliminado antes de procesarse su señal.
        pass

    if getattr(self, "_busqueda_thread", None) is thread:
        self._busqueda_thread = None
        self._busqueda_worker = None
    return True


def _esperar_hilo_busqueda(self, timeout_ms=15000):
    """Detiene una búsqueda y espera a que su hilo termine antes del cierre."""
    thread = getattr(self, "_busqueda_thread", None)
    if thread is None:
        return True
    try:
        if thread.isRunning():
            thread.requestInterruption()
            thread.quit()
            terminado = thread.wait() if timeout_ms is None else thread.wait(timeout_ms)
            if not terminado:
                log_warning("La búsqueda sigue activa durante el cierre; esperando su finalización segura.")
                thread.wait()
        if getattr(self, "_busqueda_thread", None) is thread:
            self._busqueda_thread = None
            self._busqueda_worker = None
        return True
    except RuntimeError:
        self._busqueda_thread = None
        self._busqueda_worker = None
        return True


def _normalizar_titulo_oferta(titulo):
    titulo = unicodedata.normalize("NFKD", str(titulo or ""))
    titulo = "".join(c for c in titulo if not unicodedata.combining(c)).casefold()
    titulo = re.sub(
        r"\s*[\[(]\s*(?:epic(?: games)?(?: store)?|egs|steam|gog|itch(?:\.io)?)\s*[\])]\s*$",
        "",
        titulo,
    )
    titulo = re.sub(r"\b(?:free|gratis|giveaway|on steam|on epic games|on gog)\b", " ", titulo)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", titulo).split())


def _titulos_equivalentes_entre_fuentes(titulo_a, titulo_b):
    """Reconoce títulos iguales o raíces compartidas antes de subtítulos traducidos."""
    if not str(titulo_a or "").strip() or not str(titulo_b or "").strip():
        return False
    original_a, original_b = str(titulo_a), str(titulo_b)
    normal_a = _normalizar_titulo_oferta(original_a)
    normal_b = _normalizar_titulo_oferta(original_b)
    if normal_a == normal_b:
        return True

    # El nombre de producto anterior al separador suele mantenerse aunque
    # el subtítulo cambie de idioma (p. ej., "Agent A - ..." / "Agent A: ...").
    base_a = re.split(r":\s*|\s+[-–—]\s+", original_a, maxsplit=1)[0]
    base_b = re.split(r":\s*|\s+[-–—]\s+", original_b, maxsplit=1)[0]
    if _normalizar_titulo_oferta(base_a) == _normalizar_titulo_oferta(base_b):
        return True
    return SequenceMatcher(None, normal_a, normal_b).ratio() >= 0.96


def _oferta_cache_vigente(juego, ahora_utc, cache_actualizada_utc):
    """Reutiliza solo ofertas no vencidas o sin fecha desde una caché muy reciente."""
    fecha_fin = str(juego.get("end_date") or juego.get("endDate") or "").strip()
    if not fecha_fin:
        if cache_actualizada_utc is None:
            return False
        edad = ahora_utc - cache_actualizada_utc
        return datetime.timedelta(0) <= edad <= datetime.timedelta(
            hours=_CACHE_OFERTAS_SIN_FECHA_MAX_HORAS
        )

    try:
        fecha = datetime.datetime.fromisoformat(fecha_fin.replace("Z", "+00:00"))
    except ValueError:
        return False
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=datetime.timezone.utc)
    return fecha >= ahora_utc


def _ofertas_son_equivalentes(a, b):
    tienda_a = str(_detectar_tienda_juego(a) or "").casefold().strip()
    tienda_b = str(_detectar_tienda_juego(b) or "").casefold().strip()
    if not tienda_a or tienda_a != tienda_b:
        return False
    titulo_a = str(a.get("title") or "").strip()
    titulo_b = str(b.get("title") or "").strip()
    return bool(
        titulo_a
        and titulo_b
        and _titulos_equivalentes_entre_fuentes(titulo_a, titulo_b)
    )


def _fusionar_cache_ofertas(juegos_actuales, cache, ahora_utc, cache_actualizada_utc):
    """Añade ofertas de caché vigentes que no estén ya en los resultados."""
    combinadas = list(juegos_actuales)
    recuperadas = 0
    for juego in cache:
        if not isinstance(juego, dict) or not _oferta_cache_vigente(
            juego, ahora_utc, cache_actualizada_utc
        ):
            continue
        if any(
            _ofertas_son_equivalentes(juego, actual)
            for actual in combinadas
            if isinstance(actual, dict)
        ):
            continue

        oferta = dict(juego)
        oferta.setdefault("_kg_source", "GamerPower-cache")
        combinadas.append(oferta)
        recuperadas += 1
    return combinadas, recuperadas


class _BusquedaWorker(QObject):
    terminado = Signal(object, str)
    error = Signal(str)

    def run(self):
        import requests
        juegos_encontrados = []
        respuesta_api_valida = False
        fuentes_exitosas = 0
        total_fuentes = 7

        def _obtener_gamerpower():
            response = requests.get(API_URL, headers=API_HEADERS, timeout=5.0)
            response.raise_for_status()
            datos = response.json()
            if not isinstance(datos, list):
                raise ValueError("GamerPower devolvió un formato inesperado")
            return datos

        def _ejecutar_scraper_con_sesion(fn):
            with requests.Session() as session:
                return fn(session=session)

        # Combinamos GamerPower y los scrapers para ampliar la cobertura; las
        # coincidencias entre rutas se eliminan al preparar la vista.
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
                fuentes = {
                    executor.submit(_obtener_gamerpower): "GamerPower",
                    executor.submit(_ejecutar_scraper_con_sesion, _obtener_epic_directo): "Epic Games",
                    executor.submit(_ejecutar_scraper_con_sesion, _obtener_itch_directo): "Itch.io",
                    executor.submit(_ejecutar_scraper_con_sesion, _obtener_gog_directo): "GOG",
                    executor.submit(_ejecutar_scraper_con_sesion, _obtener_steam_directo): "Steam",
                    executor.submit(_ejecutar_scraper_con_sesion, _obtener_amazon_prime_directo): "Amazon Prime",
                    executor.submit(_ejecutar_scraper_con_sesion, _obtener_fanatical_directo): "Fanatical",
                }
                completadas, pendientes = concurrent.futures.wait(
                    fuentes,
                    timeout=6.0,
                    return_when=concurrent.futures.ALL_COMPLETED,
                )
                for future in completadas:
                    fuente = fuentes[future]
                    try:
                        resultados = future.result() or []
                        fuentes_exitosas += 1
                        if fuente == "GamerPower":
                            respuesta_api_valida = True
                            if resultados:
                                _guardar_en_cache_disco(resultados)
                        for juego in resultados:
                            if isinstance(juego, dict):
                                juego.setdefault("_kg_source", fuente)
                        juegos_encontrados.extend(resultados)
                    except Exception as error_fuente:
                        log_warning(f"No se pudieron consultar ofertas en {fuente}: {error_fuente}")
                if pendientes:
                    nombres = ", ".join(fuentes[future] for future in pendientes)
                    log_warning(f"Búsqueda parcial: se agotó el tiempo para {nombres}.")
                    for future in pendientes:
                        future.cancel()

            # Completa resultados parciales por oferta, no por tienda: una
            # respuesta actual de la tienda no invalida las demás entradas de
            # caché que sigan vigentes.
            cache = _cargar_cache_otras_tiendas(
                excluir_tiendas=("Epic Games", "Itch.io", "Steam")
            ) or []
            ahora_utc = datetime.datetime.now(datetime.timezone.utc)
            try:
                cache_actualizada_utc = datetime.datetime.fromtimestamp(
                    os.path.getmtime(CACHE_GIVEAWAYS_FILE), datetime.timezone.utc
                )
            except OSError:
                cache_actualizada_utc = None
            juegos_encontrados, recuperadas = _fusionar_cache_ofertas(
                juegos_encontrados,
                cache,
                ahora_utc,
                cache_actualizada_utc,
            )
            if recuperadas:
                log_info(f"Caché: recuperadas {recuperadas} ofertas de tiendas ausentes en la respuesta actual.")
            if not respuesta_api_valida:
                log_info("GamerPower inaccesible; se muestran resultados directos y caché vigente.")
        except Exception as error_busqueda:
            log_error(f"Error en la búsqueda combinada: {error_busqueda}", exc_info=True)

        if QThread.currentThread().isInterruptionRequested():
            return
        if juegos_encontrados:
            log_info(
                f"Búsqueda combinada completada: {len(juegos_encontrados)} resultados "
                f"(API válida: {respuesta_api_valida})."
            )
            self.terminado.emit(juegos_encontrados, "combinado")
            return

        self.error.emit(_clasificar_resultado_busqueda(
            total_fuentes, fuentes_exitosas, bool(juegos_encontrados)
        ))


def _set_status(self, text, status="success"):
    self._status_kind = status
    self.status_pill.setText(text)
    es_oscuro = getattr(self, "es_modo_oscuro", config.CURRENT_THEME == "dark")
    if not es_oscuro:
        if status == "success":
            estilo = "background: #DCE9DF; color: #4D6B55; border: 1px solid #C8D9CC; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        elif status == "warning":
            estilo = "background: #EEE5D2; color: #80652F; border: 1px solid #DFD3B8; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        elif status == "error":
            estilo = "background: #EEDDD8; color: #8A514A; border: 1px solid #E0C7C1; border-radius: 10px; font-weight: bold; padding: 0 10px;"
        else:
            estilo = "background: #E0E0EC; color: #535886; border: 1px solid #CDCEE0; border-radius: 10px; font-weight: bold; padding: 0 10px;"
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
        # Ocho actualizaciones por segundo bastan para el spinner y reducen
        # trabajo de pintado durante las peticiones de red.
        timer.setInterval(125)
        timer.timeout.connect(self._actualizar_animacion_busqueda)
        self._busqueda_neon_timer = timer

    self._busqueda_neon_inicio = time.monotonic()
    self._busqueda_neon_activo = True
    self._busqueda_spinner_index = -1
    self.status_pill.setText(t("status.searching"))
    self._set_status(t("status.searching"), "info")
    if hasattr(self, "btn_actualizar"):
        self.btn_actualizar.setEnabled(False)
    timer.start()
    self._actualizar_animacion_busqueda()


def _actualizar_animacion_busqueda(self):
    if not getattr(self, "_busqueda_neon_activo", False):
        return
    transcurrido = time.monotonic() - getattr(self, "_busqueda_neon_inicio", time.monotonic())
    if hasattr(self, "btn_actualizar"):
        frames = ("◐", "◓", "◑", "◒")
        spinner_index = int(transcurrido * 8) % len(frames)
        if spinner_index != getattr(self, "_busqueda_spinner_index", -1):
            self._busqueda_spinner_index = spinner_index
            frame = frames[spinner_index]
            self.btn_actualizar.setText(f"{frame}  {t('status.searching').replace('● ', '')}")


def _detener_animacion_busqueda(self):
    self._busqueda_neon_activo = False
    timer = getattr(self, "_busqueda_neon_timer", None)
    if timer is not None:
        timer.stop()
    if hasattr(self, "btn_actualizar"):
        self.btn_actualizar.setEnabled(True)
        self.btn_actualizar.setText(t("search.button"))


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
            # API y scraper pueden titular la misma oferta de forma distinta.
            titulo = _normalizar_titulo_oferta(juego.get("title"))
            tienda = str(self._asignar_tienda(juego) or "").casefold().strip()
            clave = (tienda, titulo) if titulo else self._clave_juego(juego)

            url = str(juego.get("open_giveaway_url") or "").strip()
            url_canonica = ""
            if url:
                try:
                    partes = urlsplit(url)
                    host = (partes.hostname or "").casefold().removeprefix("www.")
                    puerto = f":{partes.port}" if partes.port else ""
                    ruta = re.sub(r"/{2,}", "/", partes.path).rstrip("/").casefold()
                    # Epic publica la misma ficha bajo prefijos regionales
                    # (/es-ES/, /en-US/, etc.). La región no identifica otra oferta.
                    if host == "store.epicgames.com":
                        ruta = re.sub(r"^/[a-z]{2}-[a-z]{2}(?=/)", "", ruta)
                    # Amazon usa una sola página de reclamaciones para todos
                    # los juegos Prime; esa URL compartida no identifica un
                    # duplicado. La clave por tienda y título sí lo hace.
                    es_pagina_generica_prime = (
                        tienda == "amazon prime"
                        and host in {"luna.amazon.com", "gaming.amazon.com"}
                        and ruta.rstrip("/") in {"/claims", "/home"}
                    )
                    if not es_pagina_generica_prime:
                        url_canonica = urlunsplit((partes.scheme.casefold() or "https", host + puerto, ruta, "", ""))
                except ValueError:
                    url_canonica = url.casefold().split("?", 1)[0].split("#", 1)[0].rstrip("/")

            duplicado_cruzado = False
            fuente = str(juego.get("_kg_source") or "")
            if tienda == "epic games" and fuente:
                for existente in juegos_unicos.values():
                    otra_fuente = str(existente.get("_kg_source") or "")
                    if (
                        otra_fuente
                        and otra_fuente != fuente
                        and self._asignar_tienda(existente) == "Epic Games"
                        and any(
                            origen.casefold().startswith("gamerpower")
                            for origen in (fuente, otra_fuente)
                        )
                        and _titulos_equivalentes_entre_fuentes(
                            existente.get("title"), juego.get("title")
                        )
                    ):
                        duplicado_cruzado = True
                        break
            if (url_canonica and url_canonica in urls_vistas) or clave in juegos_unicos or duplicado_cruzado:
                continue
            juegos_unicos[clave] = juego
            if url_canonica:
                urls_vistas.add(url_canonica)

        self.juegos_cache_global = list(juegos_unicos.values())
        conteo_tiendas = {}
        for juego in self.juegos_cache_global:
            tienda = self._asignar_tienda(juego)
            conteo_tiendas[tienda] = conteo_tiendas.get(tienda, 0) + 1
        resumen_tiendas = ", ".join(
            f"{tienda}: {cantidad}" for tienda, cantidad in sorted(conteo_tiendas.items())
        ) or "ninguna"
        log_info(f"Ofertas activas por tienda: {resumen_tiendas}.")

        # La búsqueda carga ofertas y actualiza los contadores, pero no activa
        # ni despliega tiendas por sí sola. El usuario elige qué tienda abrir.

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

        def mostrar_juegos_y_estado():
            self._detener_animacion_busqueda()
            if len(disponibles) > 0:
                self._set_status(t("status.offers", count=len(disponibles)), "success")
            else:
                self._set_status(t("status.ready"), "success")
            self._actualizar_visibilidad_atras()
            self._actualizar_vista_juegos()
            self._busqueda_en_curso = False

        mostrar_juegos_y_estado()

    except Exception as e:
        self._detener_animacion_busqueda()
        self._busqueda_en_curso = False
        log_error(f"Error procesando lista de juegos: {e}", exc_info=True)
        self._set_status("● ERROR", "error")


def _recibir_resultados_busqueda(self, giveaways, fuente):
    self._finalizar_busqueda(
        giveaways,
        getattr(self, "_busqueda_inicio", time.monotonic()),
        fuente=fuente,
    )
    _notificar_barrido_si_pendiente(self)


def _buscar_juegos_error(self, mensaje):
    self._detener_animacion_busqueda()
    self._busqueda_en_curso = False
    claves_estado = {
        "offline": ("status.offline", "error"),
        "partial": ("status.partial", "warning"),
        "empty": ("status.no_offers", "success"),
    }
    clave, tipo = claves_estado.get(mensaje, ("status.error", "error"))
    self._set_status(t(clave), tipo)
    log_warning(f"Aviso de búsqueda ({mensaje}): no se recibieron ofertas para mostrar.")
    _notificar_barrido_si_pendiente(self)


def _notificar_barrido_si_pendiente(self):
    tray = getattr(self, "_tray", None)
    if tray and getattr(tray, "_barrido_notificacion_pendiente", None) is not None:
        tray.completar_barrido()


def buscar_juegos(self):
    if getattr(self, "_busqueda_en_curso", False):
        return False

    if not self._limpiar_hilo_busqueda():
        log_warning("Se omitió una búsqueda duplicada mientras terminaba la anterior.")
        return False
    limpiar_cache_imagenes()
    self._busqueda_en_curso = True
    self._busqueda_inicio = time.monotonic()
    self._iniciar_animacion_busqueda()

    thread = QThread(self)
    worker = _BusquedaWorker()
    worker.moveToThread(thread)
    
    thread.started.connect(worker.run)
    worker.terminado.connect(self._recibir_resultados_busqueda)
    worker.error.connect(self._buscar_juegos_error)
    
    worker.terminado.connect(thread.quit)
    worker.error.connect(thread.quit)
    thread.finished.connect(worker.deleteLater)
    thread.finished.connect(self._busqueda_hilo_terminado)
    thread.finished.connect(thread.deleteLater)
    
    self._busqueda_thread = thread
    self._busqueda_worker = worker
    thread.start()
    return True


def _busqueda_hilo_terminado(self):
    """Libera referencias cuando el hilo ya no puede recibir llamadas."""
    thread = self.sender()
    if thread is getattr(self, "_busqueda_thread", None):
        self._busqueda_thread = None
        self._busqueda_worker = None


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
    from PySide6.QtCore import QParallelAnimationGroup, QSequentialAnimationGroup, QPauseAnimation

    if getattr(self, "mostrando_wishlist", False):
        self._render_wishlist()
        return

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

        # Vaciar el orden anterior antes de volver a añadir los widgets. Qt
        # reduce el índice al mover widgets que ya están dentro del layout, lo
        # que hacía que insertWidget(i, widget) emitiera avisos y dejara el orden
        # de las tarjetas inconsistente al cambiar de tienda.
        while self.frame_lista_layout.count():
            item = self.frame_lista_layout.takeAt(0)
            widget = item.widget()
            if widget is not None and widget not in self.game_widgets_map.values():
                widget.hide()
                widget.deleteLater()

        widgets_to_animate = []

        for clave in juegos_visibles_ordenados:
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
                    
            self.frame_lista_layout.addWidget(widget)
            widget.show()

        self.frame_lista_layout.addStretch(1)
        self.frame_lista_layout.activate()

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
    cls._esperar_hilo_busqueda = _esperar_hilo_busqueda
    cls._busqueda_hilo_terminado = _busqueda_hilo_terminado
    cls._set_status = _set_status
    cls._recibir_resultados_busqueda = _recibir_resultados_busqueda
    cls._buscar_juegos_error = _buscar_juegos_error
    cls._notificar_barrido_si_pendiente = _notificar_barrido_si_pendiente
    cls.buscar_juegos = buscar_juegos
    cls._actualizar_animacion_busqueda = _actualizar_animacion_busqueda
    cls._iniciar_animacion_busqueda = _iniciar_animacion_busqueda
    cls._detener_animacion_busqueda = _detener_animacion_busqueda
    cls._finalizar_busqueda = _finalizar_busqueda
    cls._asignar_tienda = _asignar_tienda
    cls.actualizar_insignias = actualizar_insignias
    cls._actualizar_visibilidad_contenedor_juegos = _actualizar_visibilidad_contenedor_juegos
    cls._actualizar_vista_juegos = _actualizar_vista_juegos




