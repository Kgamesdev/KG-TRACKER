"""Cliente de CheapShark y consultas de precios regionales de tiendas."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
import re
import unicodedata

import requests
from config import STORES_MAPPING

BASE_URL = "https://www.cheapshark.com/api/1.0"
HEADERS = {"User-Agent": "KGTracker/0.5.0 (game wishlist)"}


def _get(url: str, params: dict | None = None):
    response = requests.get(url, params=params, headers=HEADERS, timeout=12)
    response.raise_for_status()
    return response.json()


def _normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or "").casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", value))


def _title_match_score(query: str, title: str) -> float:
    normalized_query = _normalize_title(query)
    normalized_title = _normalize_title(title)
    if not normalized_query or not normalized_title:
        return 0.0
    if normalized_query in normalized_title:
        return 1.0

    query_words = normalized_query.split()
    title_words = normalized_title.split()
    word_matches = [
        max((SequenceMatcher(None, word, candidate).ratio() for candidate in title_words), default=0.0)
        for word in query_words
    ]
    coverage = sum(score >= 0.62 for score in word_matches) / max(len(query_words), 1)
    token_score = sum(word_matches) / max(len(word_matches), 1)
    whole_score = SequenceMatcher(None, normalized_query, normalized_title).ratio()
    return max(whole_score, token_score * 0.72 + coverage * 0.28)


def _search_titles(title: str) -> list[dict]:
    return _get(f"{BASE_URL}/games", {"title": title, "limit": 15})


def search_games(title: str) -> list[dict]:
    """Busca títulos y recupera candidatos cercanos si la consulta tiene erratas."""
    title = str(title or "").strip()
    if len(title) < 2:
        return []

    try:
        results = _search_titles(title)
    except requests.RequestException:
        results = []
    if results:
        ranked = sorted(results, key=lambda game: _title_match_score(title, game.get("external", "")), reverse=True)
        if _title_match_score(title, ranked[0].get("external", "")) >= 0.84:
            return ranked[:15]

    # Busca por palabras sueltas y variantes con una letra omitida. Así se
    # recuperan candidatos cuando el servicio no encuentra la errata literal.
    words = [word for word in _normalize_title(title).split() if len(word) >= 3]
    longest = max(words, key=len, default="")
    queries = []
    for word in words:
        if word not in queries:
            queries.append(word)
    deletion_variants = []
    swap_variants = []
    substitution_variants = []
    if len(longest) >= 5:
        positions = sorted(set(round(i * (len(longest) - 1) / 5) for i in range(1, 6)))
        for position in positions:
            variant = longest[:position] + longest[position + 1:]
            if len(variant) >= 3 and variant not in deletion_variants and variant not in queries:
                deletion_variants.append(variant)
        for position in range(1, len(longest) - 1):
            swapped = list(longest)
            swapped[position], swapped[position + 1] = swapped[position + 1], swapped[position]
            variant = "".join(swapped)
            if variant not in swap_variants and variant not in queries:
                swap_variants.append(variant)
        keyboard_neighbors = {
            "q": "wa", "w": "qes", "e": "wrd", "r": "etf", "t": "ryg", "y": "tuh",
            "u": "yij", "i": "uok", "o": "ipl", "p": "ol", "a": "qws", "s": "awed",
            "d": "serf", "f": "drtg", "g": "fty", "h": "gyu", "j": "huik", "k": "jiol",
            "l": "kop", "z": "asx", "x": "zsdc", "c": "xdfv", "v": "cfgb", "b": "vghn",
            "n": "bhjm", "m": "njk",
        }
        for position, char in enumerate(longest):
            neighbors = keyboard_neighbors.get(char, "")
            if neighbors:
                variant = longest[:position] + neighbors[0] + longest[position + 1:]
                if variant not in substitution_variants and variant not in queries:
                    substitution_variants.append(variant)
    variants = (
        deletion_variants[:2] + swap_variants[:1] + substitution_variants[:2]
        + deletion_variants[2:] + swap_variants[1:] + substitution_variants[2:]
    )
    queries.extend(variants[:max(0, 5 - len(queries))])
    queries = queries[:5]
    if not queries:
        return results or []

    candidates = {str(game.get("gameID")): game for game in results if game.get("gameID")}
    with ThreadPoolExecutor(max_workers=min(4, len(queries))) as executor:
        futures = [executor.submit(_search_titles, query) for query in queries]
        for future in as_completed(futures):
            try:
                for game in future.result():
                    game_id = str(game.get("gameID", ""))
                    if game_id:
                        candidates.setdefault(game_id, game)
            except requests.RequestException:
                continue

    ranked = sorted(
        candidates.values(),
        key=lambda game: _title_match_score(title, game.get("external", "")),
        reverse=True,
    )
    return ranked[:15]


def get_game_deals(game_id: str) -> dict:
    """Devuelve el producto y sus ofertas activas en las tiendas cubiertas."""
    return _get(f"{BASE_URL}/games", {"id": str(game_id)})


def _canonical_app_store(store_name: str) -> str | None:
    key = _normalize_title(store_name).replace(" ", "")
    aliases = {
        "steam": "Steam",
        "epicgames": "Epic Games",
        "epicgamesstore": "Epic Games",
        "gog": "GOG",
        "amazonprime": "Amazon Prime",
        "itchio": "Itch.io",
        "humblestore": "Humble Store",
        "humblebundle": "Humble Store",
        "fanatical": "Fanatical",
        "indiegala": "IndieGala",
    }
    canonical = aliases.get(key)
    app_stores = set(STORES_MAPPING.values()) - {"Otras Plataformas"}
    return canonical if canonical in app_stores else None


def get_stores() -> dict[str, str]:
    """Solo expone tiendas activas cuyo nombre aparece en la app."""
    allowed = {}
    for store in _get(f"{BASE_URL}/stores"):
        if not bool(int(store.get("isActive", 1) or 0)):
            continue
        canonical = _canonical_app_store(store.get("storeName", ""))
        if canonical:
            allowed[str(store["storeID"])] = canonical
    return allowed


def _amount(value) -> float | None:
    try:
        amount = float(value)
        return amount if amount >= 0 else None
    except (TypeError, ValueError):
        return None


def get_regional_prices(title: str, steam_app_id: str | None, store_names) -> dict[str, dict]:
    """Get real Spain/EUR prices where a store exposes a regional source.

    CheapShark is used for store availability and deal links, but its prices are
    USD-only. Do not currency-convert those values and present them as a local
    shop price. Steam's Spanish store response and GOG's Spain/EUR catalog are
    used for verified regional prices; other shops deliberately remain marked
    as unverified by the caller.
    """
    names = {str(name) for name in (store_names or [])}
    prices: dict[str, dict] = {}

    if "Steam" in names and str(steam_app_id or "").isdigit():
        try:
            payload = _get(
                "https://store.steampowered.com/api/appdetails",
                {"appids": str(steam_app_id), "cc": "es", "l": "spanish"},
            )
            details = payload.get(str(steam_app_id), {})
            data = details.get("data", {}) if details.get("success") else {}
            price = data.get("price_overview") or {}
            if price.get("currency") == "EUR":
                current = _amount(price.get("final"))
                retail = _amount(price.get("initial"))
                # Steam expresses these values in euro cents.
                if current is not None and retail is not None:
                    prices["Steam"] = {
                        "price_eur": round(current / 100, 2),
                        "retail_eur": round(retail / 100, 2),
                        "savings": float(price.get("discount_percent", 0) or 0),
                        "source": "Steam España",
                    }
        except (requests.RequestException, ValueError, TypeError) as exc:
            from logger import log_warning
            log_warning(f"No se pudo verificar el precio regional de Steam: {exc}")

    if "GOG" in names and title:
        try:
            payload = _get(
                "https://catalog.gog.com/v1/catalog",
                {
                    "limit": 20,
                    "countryCode": "ES",
                    "locale": "es-ES",
                    "currencyCode": "EUR",
                    "query": title,
                },
            )
            normalized_title = _normalize_title(title)
            exact_matches = [
                product for product in payload.get("products", [])
                if _normalize_title(product.get("title", "")) == normalized_title
            ]
            if exact_matches:
                product = exact_matches[0]
                price = product.get("price", {})
                current = _amount((price.get("finalMoney") or {}).get("amount"))
                retail = _amount((price.get("baseMoney") or {}).get("amount"))
                currency = (price.get("finalMoney") or {}).get("currency")
                if current is not None and retail is not None and currency == "EUR":
                    savings = max(0.0, (retail - current) / retail * 100) if retail else 0.0
                    prices["GOG"] = {
                        "price_eur": round(current, 2),
                        "retail_eur": round(retail, 2),
                        "savings": savings,
                        "source": "GOG España",
                        "url": product.get("url") or product.get("storeLink") or "",
                    }
        except (requests.RequestException, ValueError, TypeError) as exc:
            from logger import log_warning
            log_warning(f"No se pudo verificar el precio regional de GOG: {exc}")

    return prices


def deal_url(deal_id: str) -> str:
    return f"https://www.cheapshark.com/redirect?dealID={deal_id}"
