import requests
from config import API_URL, API_HEADERS, EXCLUSIONES

def get_free_games():
    """Obtiene y clasifica los juegos con las etiquetas exactas de la interfaz."""
    try:
        response = requests.get(API_URL, headers=API_HEADERS, timeout=10)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        giveaways = response.json()
    except Exception as e:
        print(f"[Error API] No se pudieron obtener las promociones: {e}")
        return []

    clean_deals = []

    for item in giveaways:
        title = item.get("title", "Juego desconocido")

        # Excluir DLCs o expansiones
        if any(exc in title.lower() for exc in EXCLUSIONES):
            continue

        raw = item.get("platforms", "").lower()

        # Coincidencia exacta con las etiquetas de la interfaz
        if "epic" in raw:
            store_name = "Epic Games"
        elif "steam" in raw:
            store_name = "Steam"
        elif "gog" in raw:
            store_name = "GOG"
        elif "prime" in raw or "amazon" in raw:
            store_name = "Amazon Prime"
        elif "itch" in raw:
            store_name = "Itch.io"
        elif "humble" in raw:
            store_name = "Humble Store"
        elif "fanatical" in raw:
            store_name = "Fanatical"
        elif "indiegala" in raw or "gala" in raw:
            store_name = "IndieGala"
        else:
            store_name = "Otras Plataformas"

        clean_deals.append({
            "title": title,
            "store_name": store_name,
            "normal_price": item.get("worth", "N/A"),
            "sale_price": "¡GRATIS!",
            "deal_link": item.get("open_giveaway_url") or item.get("gamerpower_url"),
            "thumb": item.get("image", ""),
            "description": item.get("description", ""),
            "instructions": item.get("instructions", "")
        })

    return clean_deals