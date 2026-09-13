import urllib.parse
"""Módulo centralizado de scrapers y consultas directas a tiendas de videojuegos."""

import os
import json
import datetime
import requests
import re
import html
from config import BASE_DIR

CACHE_GIVEAWAYS_FILE = os.path.join(BASE_DIR, "data", "giveaways_cache.json")


def guardar_en_cache_disco(giveaways):
    try:
        os.makedirs(os.path.dirname(CACHE_GIVEAWAYS_FILE), exist_ok=True)
        with open(CACHE_GIVEAWAYS_FILE, "w", encoding="utf-8") as f:
            json.dump(giveaways, f, ensure_ascii=False, indent=2)
    except Exception as err:
        print(f"⚠️ Error guardando caché local: {err}")


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
            print(f"⚠️ Error leyendo caché local: {err}")
    return juegos


def obtener_epic_directo():
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


def obtener_steam_directo():
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


def obtener_itch_directo():
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

            # Extracción tolerante a etiquetas internas (b, span, etc.)
            title_m = re.search(r'<div class="game_title">\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', chunk, re.DOTALL)
            if not title_m:
                continue
            url_raw = title_m.group(1).strip()
            url_juego = urllib.parse.urljoin("https://itch.io", url_raw)

            # Limpiar etiquetas HTML del título
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
        print(f"⚠️ Error consultando Itch.io directo: {err}")
    return juegos


def obtener_gog_directo():
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
