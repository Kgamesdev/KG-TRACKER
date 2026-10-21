from core.storage import guardar_json_atomico, cargar_json_seguro
import urllib.parse
"""Módulo centralizado de scrapers y consultas directas a tiendas de videojuegos."""

import os
import json
import datetime
import requests
import re
import html
import threading
import unicodedata
from html.parser import HTMLParser
from config import BASE_DIR
from core.paths import CACHE_GIVEAWAYS_FILE as USER_CACHE_GIVEAWAYS_FILE
from logger import log_info, log_warning, log_error

CACHE_GIVEAWAYS_FILE = str(USER_CACHE_GIVEAWAYS_FILE)

_session_scrapers = None
_scrapers_lock = threading.Lock()

def _obtener_sesion_scrapers():
    global _session_scrapers
    if _session_scrapers is None:
        with _scrapers_lock:
            if _session_scrapers is None:
                _session_scrapers = requests.Session()
                adapter = requests.adapters.HTTPAdapter(pool_connections=8, pool_maxsize=8)
                _session_scrapers.mount("https://", adapter)
                _session_scrapers.mount("http://", adapter)
    return _session_scrapers


def guardar_en_cache_disco(giveaways):
    try:
        os.makedirs(os.path.dirname(CACHE_GIVEAWAYS_FILE), exist_ok=True)
        guardar_json_atomico(CACHE_GIVEAWAYS_FILE, giveaways)
    except Exception as err:
        log_error(f"Error guardando caché local: {err}")


def detectar_tienda_juego(juego):
    """Determina la tienda de un juego provenga de GamerPower o de scrapers directos."""
    store_directo = juego.get("store")
    if store_directo:
        return store_directo

    platforms = str(juego.get("platforms", "")).lower()
    title = str(juego.get("title", "")).lower()
    url = str(juego.get("open_giveaway_url") or juego.get("gamerpower_url") or "").lower()
    t_str = f"{platforms} {title} {url}"

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


def cargar_cache_otras_tiendas(excluir_tiendas=("Epic Games", "Itch.io", "GOG", "Steam")):
    juegos = []
    if os.path.exists(CACHE_GIVEAWAYS_FILE):
        try:
            with open(CACHE_GIVEAWAYS_FILE, "r", encoding="utf-8-sig") as f:
                datos = json.load(f)
                if isinstance(datos, list):
                    for j in datos:
                        tienda = detectar_tienda_juego(j)
                        if tienda not in excluir_tiendas:
                            if not j.get("store"):
                                j["store"] = tienda
                            juegos.append(j)
        except Exception as err:
            log_error(f"Error leyendo caché local: {err}")
    return juegos


def obtener_epic_directo(session=None):
    """Consulta oficial a Epic Games Store validando fecha UTC activa y precio 0.00 EUR."""
    juegos = []
    try:
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        s = session or _obtener_sesion_scrapers()
        res = s.get(url, headers=headers, timeout=5)
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
            fecha_fin = ""

            for group in promo_offers:
                for off in group.get("promotionalOffers", []):
                    if off.get("discountSetting", {}).get("discountPercentage") == 0:
                        try:
                            start = datetime.datetime.fromisoformat(off["startDate"].replace("Z", "+00:00"))
                            end = datetime.datetime.fromisoformat(off["endDate"].replace("Z", "+00:00"))
                            if start <= ahora_utc <= end:
                                activa_hoy = True
                                fecha_fin = end.strftime("%Y-%m-%d %H:%M:%S")
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
                "end_date": fecha_fin,
                "published_date": "",
                "type": "Game",
                "platforms": "PC",
                "store": "Epic Games",
            })
    except Exception as err:
        log_error(f"Error consultando Epic Games directo: {err}")
    return juegos


def obtener_steam_directo(session=None):
    """Consulta oficial a Steam filtrando ofertas temporales al 100% de descuento activas."""
    juegos = []
    try:
        url = "https://store.steampowered.com/api/featuredcategories"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        s = session or _obtener_sesion_scrapers()
        res = s.get(url, headers=headers, timeout=5)
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
        log_error(f"Error consultando Steam directo: {err}")
    return juegos


def obtener_itch_directo(session=None):
    """Consulta oficial a Itch.io filtrando ofertas activas al 100% de descuento."""
    juegos = []
    try:
        url = "https://itch.io/games/on-sale?format=json"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        s = session or _obtener_sesion_scrapers()
        res = s.get(url, headers=headers, timeout=6)
        if res.status_code != 200:
            return []
        data = res.json()
        content_html = data.get("content", "")
        chunks = content_html.split('data-game_id="')[1:]

        for chunk in chunks:
            if "-100%" not in chunk and 'class="price_value">$0</div>' not in chunk:
                continue

            game_id = chunk.split('"')[0]

            title_m = re.search(r'<div class="game_title">\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', chunk, re.DOTALL)
            if not title_m:
                continue
            url_raw = title_m.group(1).strip()
            url_juego = urllib.parse.urljoin("https://itch.io", url_raw)

            titulo_raw = re.sub(r'<[^>]+>', '', title_m.group(2))
            titulo = html.unescape(titulo_raw).strip()
            if not titulo:
                continue

            img_m = re.search(r'data-lazy_src="([^"]+)"', chunk) or re.search(r'src="([^"]+)"', chunk)
            imagen = img_m.group(1).strip() if img_m else None
            if imagen:
                if imagen.startswith("//"):
                    imagen = "https:" + imagen
                elif not imagen.startswith("http"):
                    imagen = urllib.parse.urljoin("https://itch.io", imagen)

            desc_m = re.search(r'class="game_text"[^>]*title="([^"]+)"', chunk) or re.search(r'class="game_text"[^>]*>(.*?)</div>', chunk, re.DOTALL)
            if desc_m:
                desc_limpia = re.sub(r'<[^>]+>', '', desc_m.group(1))
                desc = html.unescape(desc_limpia).strip()
            else:
                desc = f"Oferta 100% gratuita en Itch.io: {titulo}"

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
        log_error(f"Error consultando Itch.io directo: {err}")
    return juegos


def obtener_gog_directo(session=None):
    """Consulta ofertas gratis de GOG con un endpoint web alternativo."""
    juegos = []
    s = session or _obtener_sesion_scrapers()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
    }
    endpoints = (
        (
            "https://catalog.gog.com/v1/catalog",
            {"limit": 48, "price": "between:0,0", "order": "desc:trending",
             "discounted": "eq:true", "productType": "in:game,pack", "page": 1,
             "countryCode": "ES", "locale": "es-ES", "currencyCode": "EUR"},
        ),
        (
            "https://www.gog.com/games/ajax/filtered",
            {"mediaType": "game", "price": "free", "page": 1, "sort": "popularity"},
        ),
    )

    for url, params in endpoints:
        try:
            res = s.get(url, params=params, headers=headers, timeout=6)
            if res.status_code != 200:
                log_warning(f"GOG devolvió HTTP {res.status_code} en {res.url}.")
                continue
            try:
                data = res.json()
            except (ValueError, json.JSONDecodeError):
                # El endpoint web puede devolver JSON incrustado en HTML.
                match = re.search(r'\{.*"products"\s*:\s*\[.*\].*\}', res.text, re.DOTALL)
                if not match:
                    continue
                data = json.loads(match.group(0))
            products = data.get("products") or data.get("items") or []
            for p in products:
                price_info = p.get("price") or {}
                final_money = price_info.get("finalMoney") or {}
                base_money = price_info.get("baseMoney") or {}
                try:
                    final_val = float(final_money.get("amount", price_info.get("finalAmount", -1)))
                    base_val = float(base_money.get("amount", price_info.get("baseAmount", 0)))
                except (ValueError, TypeError):
                    continue
                if final_val != 0.0 or base_val <= 0.0:
                    continue

                titulo = str(p.get("title") or p.get("name") or "").strip()
                slug = str(p.get("slug") or "").strip()
                if not titulo:
                    continue
                link = p.get("storeLink") or p.get("url") or (f"https://www.gog.com/game/{slug}" if slug else "https://www.gog.com/games?price=free")
                if str(link).startswith("/"):
                    link = urllib.parse.urljoin("https://www.gog.com", link)
                img = p.get("coverHorizontal") or p.get("coverVertical") or p.get("image")
                juegos.append({
                    "id": f"gog_{p.get('id', slug or titulo)}", "title": titulo,
                    "worth": f"€{base_val:.2f}", "worth_value": base_val,
                    "thumbnail": img, "image": img,
                    "description": f"Juego gratuito con 100% de descuento en GOG: {titulo}.",
                    "instructions": "Reclama el juego gratis para siempre en GOG.",
                    "open_giveaway_url": link, "published_date": "", "type": "Game",
                    "platforms": "PC, DRM-Free", "store": "GOG",
                })
            if juegos:
                break
        except Exception as err:
            log_warning(f"No respondió la ruta de GOG {url}: {err}")
    return juegos


class _AmazonArticleText(HTMLParser):
    """Extrae texto por elemento de lista de los artículos públicos de Amazon."""

    def __init__(self):
        super().__init__()
        self.items = []
        self._depth = 0
        self._parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            if self._depth == 0:
                self._parts = []
            self._depth += 1
        elif self._depth:
            self._parts.append(" ")

    def handle_endtag(self, tag):
        if tag == "li" and self._depth:
            self._depth -= 1
            if self._depth == 0:
                value = " ".join("".join(self._parts).split())
                if value:
                    self.items.append(value)

    def handle_data(self, data):
        if self._depth:
            self._parts.append(data)


def _obtener_enlaces_individuales_prime(session):
    """Lee enlaces de reclamo Luna individualizados desde su índice público."""
    url = "https://www.couchloot.com/free"
    try:
        response = session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"},
            timeout=4,
        )
        if response.status_code != 200:
            return {}
        enlaces = {}
        scripts = re.findall(
            r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script\s*>',
            response.text,
            re.IGNORECASE | re.DOTALL,
        )

        def recorrer(value):
            if isinstance(value, dict):
                name, target = value.get("name"), value.get("url")
                if isinstance(name, str) and isinstance(target, str):
                    parsed = urllib.parse.urlsplit(target)
                    if parsed.scheme == "https" and parsed.hostname == "luna.amazon.com" and parsed.path.startswith("/claims/"):
                        normalizado = unicodedata.normalize("NFKD", name.casefold())
                        normalizado = "".join(c for c in normalizado if not unicodedata.combining(c))
                        normalizado = " ".join(re.findall(r"[a-z0-9]+", normalizado))
                        enlaces[normalizado] = target
                for child in value.values():
                    recorrer(child)
            elif isinstance(value, list):
                for child in value:
                    recorrer(child)

        for source in scripts:
            try:
                recorrer(json.loads(html.unescape(source)))
            except (ValueError, TypeError):
                continue
        return enlaces
    except Exception as err:
        log_warning(f"No se pudieron resolver enlaces individuales de Amazon Prime: {err}")
        return {}


def obtener_amazon_prime_directo(session=None):
    """Lee las ofertas PC anunciadas públicamente por Amazon Luna/Prime.

    Prime muestra varias semanas de ofertas a la vez. Como los artículos
    públicos anuncian la fecha de inicio pero no siempre el fin de reclamación,
    conservamos las ofertas de las últimas cinco semanas y dejamos vacío el
    fin para no inventar una fecha exacta.
    """
    s = session or _obtener_sesion_scrapers()
    hoy = datetime.datetime.now(datetime.timezone.utc).date()
    meses = ("january", "february", "march", "april", "may", "june",
             "july", "august", "september", "october", "november", "december")
    inicio_mes = hoy.replace(day=1)
    mes_anterior = (inicio_mes - datetime.timedelta(days=1)).replace(day=1)
    url_mes = lambda d: f"https://www.amazongamestudios.com/en-us/news/articles/luna-{meses[d.month - 1]}-{d.year}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
    resultado = {}
    patron = re.compile(
        r"^(?P<title>.+?)\s*\((?P<date>January|February|March|April|May|June|July|August|September|October|November|December)\s+(?P<day>\d{1,2})(?:,\s*(?P<delivery>[^)]+))?\)$",
        re.IGNORECASE,
    )

    for fecha_mes in (inicio_mes, mes_anterior):
        article_url = url_mes(fecha_mes)
        try:
            response = s.get(article_url, headers=headers, timeout=7)
            if response.status_code != 200:
                log_warning(f"Amazon Prime devolvió HTTP {response.status_code} en el artículo mensual.")
                continue
            parser = _AmazonArticleText()
            parser.feed(response.text)
            for item in parser.items:
                match = patron.match(item)
                if not match:
                    continue
                title = html.unescape(match.group("title")).strip()
                month_num = meses.index(match.group("date").casefold()) + 1
                year = fecha_mes.year
                if fecha_mes.month == 12 and month_num == 1:
                    year += 1
                elif fecha_mes.month == 1 and month_num == 12:
                    year -= 1
                try:
                    start_date = datetime.date(year, month_num, int(match.group("day")))
                except ValueError:
                    continue
                if not title or start_date > hoy or (hoy - start_date).days > 35:
                    continue
                delivery = (match.group("delivery") or "PC").strip()
                key = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-")
                result = {
                    "id": f"amazon_prime_{start_date.isoformat()}_{key}",
                    "title": title,
                    "worth": "Gratis con Prime",
                    "worth_value": 0.0,
                    "thumbnail": None,
                    "image": None,
                    "description": f"Oferta de Prime Gaming. Canje mediante: {delivery}.",
                    "instructions": "Reclama el juego desde Amazon Luna con una suscripción Prime.",
                    "open_giveaway_url": "https://luna.amazon.com/claims",
                    "published_date": start_date.isoformat(),
                    "end_date": "",
                    "type": "Game",
                    "platforms": f"PC, Amazon Prime — {delivery}",
                    "store": "Amazon Prime",
                    "_kg_source": "Amazon Luna / Prime",
                }
                resultado[result["id"]] = result
        except Exception as err:
            log_warning(f"No se pudieron consultar ofertas de Amazon Prime ({article_url}): {err}")

    # El anuncio de Amazon enlaza a una página general. Este índice público
    # añade los deep links oficiales de Luna; solo aceptamos destinos en
    # luna.amazon.com y los asociamos por título exacto normalizado.
    enlaces_individuales = _obtener_enlaces_individuales_prime(s)
    for oferta in resultado.values():
        normalizado = unicodedata.normalize("NFKD", oferta["title"].casefold())
        normalizado = "".join(c for c in normalizado if not unicodedata.combining(c))
        normalizado = " ".join(re.findall(r"[a-z0-9]+", normalizado))
        oferta["open_giveaway_url"] = enlaces_individuales.get(
            normalizado, oferta["open_giveaway_url"]
        )

    ofertas = list(resultado.values())
    if ofertas:
        log_info(f"Amazon Prime: encontradas {len(ofertas)} ofertas PC anunciadas recientemente.")
    return ofertas


def obtener_fanatical_directo(session=None):
    """Busca sorteos de juego gratis activos publicados por Fanatical."""
    s = session or _obtener_sesion_scrapers()
    terms_url = "https://support.fanatical.com/hc/en-us/articles/360018002197-Promotions-Summary-Terms-and-Conditions"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
    try:
        terms_response = s.get(terms_url, headers=headers, timeout=5)
        if terms_response.status_code != 200:
            log_warning(f"Fanatical devolvió HTTP {terms_response.status_code} en sus condiciones de promociones.")
            return []
    except Exception as err:
        log_warning(f"No se pudieron consultar las promociones de Fanatical: {err}")
        return []

    headings = list(re.finditer(r"<h[1-4]\b[^>]*>(.*?)</h[1-4]\s*>", terms_response.text, re.IGNORECASE | re.DOTALL))
    ahora = datetime.datetime.now(datetime.timezone.utc)
    ofertas = []
    patron_fecha = re.compile(
        r"(?:Date of promotion|Promotion starts?)\s*:\s*(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+(?P<month>[A-Za-z]+)\s+(?P<year>\d{4}),?\s*(?P<time>\d{1,2}:\d{2}\s*[AP]M)\s*GMT",
        re.IGNORECASE,
    )
    patron_fin = re.compile(
        r"End\s*:\s*(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+(?P<month>[A-Za-z]+)\s+(?P<year>\d{4}),?\s*(?P<time>\d{1,2}:\d{2}\s*[AP]M)\s*GMT",
        re.IGNORECASE,
    )

    for index, heading in enumerate(headings):
        titulo_seccion = html.unescape(re.sub(r"<[^>]+>", " ", heading.group(1)))
        if not re.search(r"free\s+game\s+giveaway", titulo_seccion, re.IGNORECASE):
            continue
        fin_seccion = headings[index + 1].start() if index + 1 < len(headings) else len(terms_response.text)
        contenido_html = terms_response.text[heading.end():fin_seccion]
        contenido = html.unescape(re.sub(r"<[^>]+>", " ", contenido_html))
        contenido = " ".join(contenido.split())
        titulo_match = re.search(r"Promotion\s*:\s*Get\s+(.+?)\s+for\s+free", contenido, re.IGNORECASE)
        if not titulo_match:
            continue
        titulo = titulo_match.group(1).strip(" .!\u00a0")
        fecha_inicio = patron_fecha.search(contenido)
        fecha_fin = patron_fin.search(contenido)
        if not fecha_inicio or not fecha_fin:
            continue

        def parsear_fecha(match):
            try:
                valor = datetime.datetime.strptime(
                    f"{match.group('day')} {match.group('month')} {match.group('year')} {match.group('time').upper()}",
                    "%d %B %Y %I:%M %p",
                )
                return valor.replace(tzinfo=datetime.timezone.utc)
            except ValueError:
                return None

        inicio, fin = parsear_fecha(fecha_inicio), parsear_fecha(fecha_fin)
        if not inicio or not fin or not inicio <= ahora <= fin:
            continue

        producto_match = re.search(
            r"href=[\"'](?P<url>(?:https://www\.fanatical\.com)?/(?:en/)?game/[^\"']+)[\"']",
            contenido_html,
            re.IGNORECASE,
        )
        slug = re.sub(r"[^a-z0-9]+", "-", titulo.casefold()).strip("-")
        producto_url = (
            urllib.parse.urljoin("https://www.fanatical.com", producto_match.group("url"))
            if producto_match else f"https://www.fanatical.com/en/game/{slug}"
        )
        try:
            producto_response = s.get(producto_url, headers=headers, timeout=5)
            if producto_response.status_code != 200:
                continue
            texto_producto = html.unescape(re.sub(r"<[^>]+>", " ", producto_response.text)).casefold()
            if "sorry, you've missed out" in texto_producto or "sorry, you’ve missed out" in texto_producto:
                continue
            if not re.search(r"free game giveaway|for free|free giveaway", texto_producto):
                continue
        except Exception as err:
            log_warning(f"No se pudo verificar la promoción Fanatical de {titulo}: {err}")
            continue

        imagen_match = re.search(
            r'<meta\b[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)',
            producto_response.text,
            re.IGNORECASE,
        )
        imagen = html.unescape(imagen_match.group(1)) if imagen_match else None
        ofertas.append({
            "id": f"fanatical_{slug}",
            "title": titulo,
            "worth": "Gratis",
            "worth_value": 0.0,
            "thumbnail": imagen,
            "image": imagen,
            "description": f"Sorteo gratuito temporal de Fanatical. Consulta las condiciones y restricciones regionales.",
            "instructions": "Reclama el juego desde la página de Fanatical durante la promoción.",
            "open_giveaway_url": producto_url,
            "published_date": inicio.strftime("%Y-%m-%d"),
            "end_date": fin.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Game",
            "platforms": "PC, Steam",
            "store": "Fanatical",
            "_kg_source": "Fanatical",
        })

    if ofertas:
        log_info(f"Fanatical: encontradas {len(ofertas)} promociones gratuitas activas.")
    else:
        log_info("Fanatical: no hay promociones gratuitas activas verificables ahora mismo.")
    return ofertas


