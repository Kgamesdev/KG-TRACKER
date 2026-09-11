"""Motor de internacionalizacion (i18n) para textos de KG Tracker."""

import os
import json
from config import BASE_DIR

SETTINGS_FILE = os.path.join(BASE_DIR, "data", "settings.json")

IDIOMAS = {
    "es": "Español (ES)",
    "en": "English (EN)",
}

MAPEO_FRECUENCIA = {
    "es": ["Cada 2 horas", "Cada 4 horas", "Cada 8 horas", "Una vez al día (24h)", "Solo al iniciar", "Desactivado"],
    "en": ["Every 2 hours", "Every 4 hours", "Every 8 hours", "Once a day (24h)", "Only at startup", "Disabled"],
}

MAPEO_TEMAS = {
    "es": ["Neón Cyberpunk (Oscuro)", "Minimalista Claro"],
    "en": ["Neon Cyberpunk (Dark)", "Minimalist Light"],
}

TRADUCCIONES = {
    "es": {
        "app.title": "K GAME TRACKER",
        "search.button": "BUSCAR JUEGOS GRATUITOS",
        "status.ready": "● LISTO",
        "status.offers": "● {count} OFERTAS",
        "status.claimed": "● {count} RECLAMADOS",
        "status.error": "● ERROR",
        "status.searching": "● BUSCANDO...",
        "claimed.btn": "★ RECLAMADOS",
        "claimed.btn_active": "★ VER RECLAMADOS",
        "claimed.title": "★  MIS RECLAMADOS  ·  {count}",
        "claimed.empty": "AÚN NO TIENES JUEGOS RECLAMADOS",
        "saved.pill": "$ AHORRADO : {amount}",
        "card.claim": "RECLAMAR",
        "card.claimed": "RECLAMADO",
        "card.unclaimed": "NO RECLAMADO",
        "card.estimated_worth": "VALOR ESTIMADO: ${worth}",
        "card.no_thumbnail": "SIN\nMINIATURA",
        "card.loading_thumbnail": "CARGANDO...",
        "card.no_desc": "Sin descripción disponible.",
        "volume.label": "VOLUMEN",
        "store.empty": "No hay elementos disponibles en {store} actualmente.",
        "store.offers_count": "{count} ofertas",
        "sidebar.select_all": "Seleccionar todas",
        "sidebar.deselect_all": "Deseleccionar todas",
        "settings.title": "AJUSTES",
        "settings.freq_label": "Buscar ofertas automáticamente",
        "settings.lang_label": "Idioma de la interfaz",
        "settings.theme_label": "Tema visual",
        "settings.autostart_label": "Iniciar con Windows (minimizado)",
        "settings.notif_label": "Mostrar notificaciones de ofertas",
        "settings.save_btn": "GUARDAR CAMBIOS",
        "kofi.title": "☕ ¿Apoyar el proyecto?",
        "kofi.desc": "K Game Tracker es gratuito y se mantiene con esfuerzo.\n¡Invítame a un café! :)",
        "kofi.continue": "Continuar a Ko-fi",
        "kofi.cancel": "Cancelar",

        # Notificaciones y System Tray (ES)
        "tray.tooltip": "K Game Tracker — Ofertas activas",
        "tray.menu_open": "Mostrar K Game Tracker",
        "tray.menu_check": "Comprobar ofertas ahora",
        "tray.menu_exit": "Salir completamente",
        "tray.minimized_title": "K Game Tracker minimizado",
        "tray.minimized_body_offers": "Tienes {count} ofertas disponibles sin reclamar. Haz clic aquí para verlas.",
        "tray.minimized_body_uptodate": "¡Al día! Ya has reclamado todas las ofertas disponibles.",
        "tray.sweep_manual_title": "Barrido de ofertas completado",
        "tray.sweep_auto_title": "Actualización de ofertas",
        "tray.sweep_body_offers": "Se encontraron {count} ofertas pendientes de reclamar.",
        "tray.sweep_body_none": "Estás al día. No hay ofertas nuevas pendientes.",
    },
    "en": {
        "app.title": "K GAME TRACKER",
        "search.button": "SEARCH FREE GAMES",
        "status.ready": "● READY",
        "status.offers": "● {count} OFFERS",
        "status.claimed": "● {count} CLAIMED",
        "status.error": "● ERROR",
        "status.searching": "● SEARCHING...",
        "claimed.btn": "★ CLAIMED",
        "claimed.btn_active": "★ VIEW CLAIMED",
        "claimed.title": "★  MY CLAIMED  ·  {count}",
        "claimed.empty": "YOU DON'T HAVE ANY CLAIMED GAMES YET",
        "saved.pill": "$ SAVED : {amount}",
        "card.claim": "CLAIM",
        "card.claimed": "CLAIMED",
        "card.unclaimed": "UNCLAIMED",
        "card.estimated_worth": "ESTIMATED VALUE: ${worth}",
        "card.no_thumbnail": "NO\nTHUMBNAIL",
        "card.loading_thumbnail": "LOADING...",
        "card.no_desc": "No description available.",
        "volume.label": "VOLUME",
        "store.empty": "No items currently available in {store}.",
        "store.offers_count": "{count} offers",
        "sidebar.select_all": "Select all",
        "sidebar.deselect_all": "Deselect all",
        "settings.title": "SETTINGS",
        "settings.freq_label": "Check for offers automatically",
        "settings.lang_label": "Interface language",
        "settings.theme_label": "Visual theme",
        "settings.autostart_label": "Start with Windows (minimized)",
        "settings.notif_label": "Show desktop notifications",
        "settings.save_btn": "SAVE CHANGES",
        "kofi.title": "☕ Support the project?",
        "kofi.desc": "K Game Tracker is free and maintained with care.\nBuy me a coffee! :)",
        "kofi.continue": "Continue to Ko-fi",
        "kofi.cancel": "Cancel",

        # Notificaciones y System Tray (EN)
        "tray.tooltip": "K Game Tracker — Active offers",
        "tray.menu_open": "Open K Game Tracker",
        "tray.menu_check": "Check for offers now",
        "tray.menu_exit": "Exit application",
        "tray.minimized_title": "K Game Tracker minimized",
        "tray.minimized_body_offers": "You have {count} unclaimed offers available. Click here to view them.",
        "tray.minimized_body_uptodate": "All caught up! You've claimed all available offers.",
        "tray.sweep_manual_title": "Offer scan completed",
        "tray.sweep_auto_title": "Offers update",
        "tray.sweep_body_offers": "Found {count} pending offers to claim.",
        "tray.sweep_body_none": "You're all set. No new pending offers.",
    }
}

_idioma_actual = "es"


def obtener_idioma() -> str:
    global _idioma_actual
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang_raw = str(data.get("idioma", "es")).lower()
                lang_code = str(data.get("idioma_codigo", "")).lower()
                if lang_code in ("en", "es"):
                    _idioma_actual = lang_code
                elif "en" in lang_raw or "english" in lang_raw:
                    _idioma_actual = "en"
                else:
                    _idioma_actual = "es"
        except Exception:
            _idioma_actual = "es"
    return _idioma_actual


def establecer_idioma(lang_code: str):
    global _idioma_actual
    _idioma_actual = lang_code if lang_code in TRADUCCIONES else "es"


def t(clave: str, **kwargs) -> str:
    lang = obtener_idioma()
    texto = TRADUCCIONES.get(lang, {}).get(clave)
    if texto is None:
        texto = TRADUCCIONES.get("es", {}).get(clave, clave)
    if kwargs:
        try:
            return texto.format(**kwargs)
        except Exception:
            return texto
    return texto
