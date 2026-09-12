"""Búsqueda, filtrado y construcción de la vista de juegos con validación temporal estricta a 0.00 EUR."""

import os
import json
import time
import datetime
import requests
import re
import html
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
from ui.game_card import GameCard
from core.i18n import t

CACHE_GIVEAWAYS_FILE = os.path.join(BASE_DIR, "data", "giveaways_cache.json")


def _limpiar_hilo_busqueda(self):
    if hasattr(self, "_busqueda_thread") and self._busqueda_thread:
        if self._busqueda_thread.isRunning():
            self._busqueda_thread.quit()
            self._busqueda_thread.wait(500)
        self._busqueda_thread = None
    self._busqueda_worker = None


def _guardar_en_cache_disco(giveaways):
    try:
        os.makedirs(os.path.dirname(CACHE_GIVEAWAYS_FILE), exist_ok=True)
        with open(CACHE_GIVEAWAYS_FILE, "w", encoding="utf-8") as f:
            json.dump(giveaways, f, ensure_ascii=False, indent=2)
    except Exception as err:
        print(f"⚠️ Error guardando caché local: {err}")


def _cargar_cache_otras_tiendas(excluir_tiendas=("Epic Games", "Itch.io", "GOG", "Steam")):
    juegos = []
    if os.path.exists(CACHE_GIVEAWAYS_FILE):
        try:
            with open(CACHE_GIVEAWAYS_FILE, "r", encoding="utf-8-sig") as f:
                datos = json.load(f)
                if isinstance(datos, list):
                    for j in datos:
                        if j.get("store") not in excluir_tiendas:
                            juegos.append(j)
        except Exception as err:
            print(f"⚠️ Error leyendo caché local: {err}")
    return juegos


def _obtener_epic_directo():
    """Consulta oficial a Epic Games Store validando fecha UTC activa y precio 0.00 EUR."""
    juegos = []
    try:
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code != 200:
            return []
        data = res.json()
        elements = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
        ahora_utc = datetime.datetime.now(datetime.timezone.utc)

        for el in elements:
            price_info = el.get("price", {}).get("totalPrice", {})
            original_price_cents = price_info.get("originalPrice", 0)
            if original_price_cents <= 0:
                continue

            promotions = el.get("promotions") or {}
            promo_offers = promotions.get("promotionalOffers") or []
            activa_hoy = False

            for group in promo_offers:
                for off in group.get("promotionalOffers", []):
                    # Descuento del 100% (discountPercentage == 0 en el setting de Epic)
                    if off.get("discountSetting", {}).get("discountPercentage") == 0:
                        try:
                            start = datetime.datetime.fromisoformat(off["startDate"].replace("Z", "+00:00"))
                            end = datetime.datetime.fromisoformat(off["endDate"].replace("Z", "+00:00"))
                            if start <= ahora_utc <= end:
                                activa_hoy = True
                                break
                        except Exception:
                            pass
                if activa_hoy:
                    break

            if not activa_hoy:
                continue

            title = str(el.get("title") or "").strip()
            if not title:
                continue

            desc = str(el.get("description") or "").strip()
            worth_val = round(original_price_cents / 100.0, 2)
            worth_str = f"${worth_val:.2f}"

            thumb = None
            for img in el.get("keyImages", []):
                if img.get("type") in ("OfferImageWide", "Thumbnail", "DieselStoreFrontWide"):
                    thumb = img.get("url")
                    break
            if not thumb and el.get("keyImages"):
                thumb = el.get("keyImages")[0].get("url")

            # Resolución canónica del enlace directo
            slug = None
            mappings = el.get("offerMappings") or []
            if mappings and mappings[0].get("pageSlug"):
                slug = mappings[0].get("pageSlug")
            elif el.get("productSlug"):
                slug = el.get("productSlug")
            elif el.get("urlSlug"):
                slug = el.get("urlSlug")

            giveaway_url = f"https://store.epicgames.com/es-ES/p/{slug}" if slug else "https://store.epicgames.com/free-games"

            juegos.append({
                "id": f"epic_{el.get('id', title)}",
                "title": title,
                "worth": worth_str,
                "worth_value": worth_val,
                "thumbnail": thumb,
                "image": thumb,
                "description": desc,
                "instructions": "Reclama el juego gratis en la tienda de Epic Games.",
                "open_giveaway_url": giveaway_url,
                "published_date": "",
                "type": "Game",
                "platforms": "PC",
                "store": "Epic Games",
            })
    except Exception as err:
        print(f"⚠️ Error consultando Epic Games directo: {err}")
    return juegos


def _obtener_steam_directo():
    """Consulta oficial a Steam filtrando ofertas temporales al 100% de descuento activas."""
    juegos = []
    try:
        url = "https://store.steampowered.com/api/featuredcategories"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            specials = data.get("specials", {}).get("items", [])
            for it in specials:
                orig_cents = it.get("original_price", 0)
                final_cents = it.get("final_price", -1)
                discount_pct = it.get("discount_percent", 0)
                if orig_cents > 0 and (final_cents == 0 or discount_pct == 100):
                    worth_val = round(orig_cents / 100.0, 2)
                    juegos.append({
                        "id": f"steam_{it.get('id')}",
                        "title": it.get("name"),
                        "worth": f"${worth_val:.2f}",
                        "worth_value": worth_val,
                        "thumbnail": it.get("header_image"),
                        "image": it.get("header_image"),
                        "description": f"Oferta 100% gratuita en Steam: {it.get('name')}.",
                        "instructions": "Añádelo gratis a tu cuenta de Steam para siempre.",
                        "open_giveaway_url": f"https://store.steampowered.com/app/{it.get('id')}/",
                        "published_date": "",
                        "type": "Game",
                        "platforms": "PC, Steam",
                        "store": "Steam",
                    })
    except Exception as err:
        print(f"⚠️ Error consultando Steam directo: {err}")
    return juegos




def _obtener_itch_directo():
    """Consulta oficial a Itch.io filtrando ofertas activas al 100% de descuento."""
    juegos = []
    try:
        url = "https://itch.io/games/on-sale?format=json"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code != 200:
            return []
        data = res.json()
        content_html = data.get("content", "")
        chunks = content_html.split('data-game_id="')[1:]

        for chunk in chunks:
            if "-100%" not in chunk and 'class="price_value">$0</div>' not in chunk:
                continue

            game_id = chunk.split('"')[0]

            title_m = re.search(r'<div class="game_title">\s*<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', chunk)
            if not title_m:
                continue
            url_juego = title_m.group(1)
            titulo = html.unescape(title_m.group(2).strip())

            img_m = re.search(r'data-lazy_src="([^"]+)"', chunk) or re.search(r'src="([^"]+)"', chunk)
            imagen = img_m.group(1) if img_m else None

            desc_m = re.search(r'class="game_text"[^>]*title="([^"]+)"', chunk) or re.search(r'class="game_text"[^>]*>([^<]+)<', chunk)
            desc = html.unescape(desc_m.group(1).strip()) if desc_m else f"Oferta 100% gratuita en Itch.io: {titulo}"

            juegos.append({
                "id": f"itch_{game_id}",
                "title": titulo,
                "worth": "100% OFF",
                "worth_value": 0.0,
                "thumbnail": imagen,
                "image": imagen,
                "description": desc,
                "instructions": "Reclama o descarga gratis en Itch.io.",
                "open_giveaway_url": url_juego,
                "published_date": "",
                "type": "Game",
                "platforms": "PC",
                "store": "Itch.io",
            })
    except Exception as err:
        print(f"⚠️ Error consultando Itch.io directo: {err}")
    return juegos


def _obtener_gog_directo():
    """Consulta oficial a GOG catalogando ofertas activas con 100% de descuento."""
    juegos = []
    try:
        url = "https://catalog.gog.com/v1/catalog?limit=48&order=desc:bestselling&discounted=eq:true"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code != 200:
            return []
        data = res.json()
        products = data.get("products", [])

        for p in products:
            price_info = p.get("price") or {}
            final_money = price_info.get("finalMoney") or {}
            base_money = price_info.get("baseMoney") or {}

            try:
                final_val = float(final_money.get("amount", -1))
                base_val = float(base_money.get("amount", 0))
            except (ValueError, TypeError):
                continue

            if final_val == 0.0 and base_val > 0.0:
                titulo = p.get("title", "").strip()
                slug = p.get("slug", "")
                link = p.get("storeLink") or f"https://www.gog.com/game/{slug}"
                img = p.get("coverHorizontal") or p.get("coverVertical")

                juegos.append({
                    "id": f"gog_{p.get('id', slug)}",
                    "title": titulo,
                    "worth": f"${base_val:.2f}",
                    "worth_value": base_val,
                    "thumbnail": img,
                    "image": img,
                    "description": f"Juego gratuito con 100% de descuento en GOG: {titulo}.",
                    "instructions": "Reclama el juego gratis para siempre en GOG.",
                    "open_giveaway_url": link,
                    "published_date": "",
                    "type": "Game",
                    "platforms": "PC, DRM-Free",
                    "store": "GOG",
                })
    except Exception as err:
        print(f"⚠️ Error consultando GOG directo: {err}")
    return juegos

class _BusquedaWorker(QObject):
    terminado = Signal(object, str)
    error = Signal(str)

    def run(self):
        # 1. Proveedor principal (GamerPower) con timeout ultra-ágil (1.2s)
        try:
            response = requests.get(API_URL, headers=API_HEADERS, timeout=(1.2, 2.5))
            response.raise_for_status()
            giveaways = response.json()
            if isinstance(giveaways, list) and len(giveaways) > 0:
                _guardar_en_cache_disco(giveaways)
                self.terminado.emit(giveaways, "gamerpower")
                return
        except Exception as e:
            print(f"⚠️ GamerPower inaccesible ({e}).")
            print("🔄 Activando motor oficial de tiendas directas...")

        # 2. Motor Oficial: Concurrencia multitienda (Epic, Itch.io, GOG, Steam) + Caché legítima
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
                        print(f"⚠️ Error en subfuente directa: {err_f}")

            tiendas_vivas = ("Epic Games", "Itch.io", "GOG", "Steam")
            juegos_otras_tiendas = _cargar_cache_otras_tiendas(excluir_tiendas=tiendas_vivas)
            if juegos_otras_tiendas:
                juegos_hibridos.extend(juegos_otras_tiendas)

            if juegos_hibridos:
                print(f"✅ Motor completado: {len(juegos_hibridos)} juegos a 0,00 EUR confirmados.")
                self.terminado.emit(juegos_hibridos, "hibrido")
                return
        except Exception as err_hibrido:
            print(f"❌ Error en motor: {err_hibrido}")

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
        print(f"❌ Error procesando lista de juegos: {e}")
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
    print(f"⚠️ Aviso de búsqueda: {mensaje}")


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

        if getattr(self, "mostrando_reclamados", False):
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
            header_button = QPushButton(f"{arrow}  {store.upper()}")
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