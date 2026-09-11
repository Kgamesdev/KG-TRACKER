"""Configuración y constantes globales de la aplicación."""

import os

# --- RUTAS DE ARCHIVOS Y RECURSOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_PATH = os.path.join(ASSETS_DIR, "logo.ico")
LOGO_PATH = os.path.join(ASSETS_DIR, "LogoKG_transparente.png")

# --- API ---
API_URL = "https://www.gamerpower.com/api/giveaways?type=game"
API_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# --- Palabras que excluyen un giveaway (DLC, addons, etc.) ---
EXCLUSIONES = [
    "dlc", "soundtrack", "ost", "expansion", "season pass",
    "add-on", "pack", "bundle", "upgrade", "beta", "alpha"
]

# --- MAPEO DE TIENDAS (ÚNICA FUENTE DE VERDAD) ---
STORES_MAPPING = {
    "epic-games-store": "Epic Games",
    "steam": "Steam",
    "gog": "GOG",
    "amazon": "Amazon Prime",
    "itchio": "Itch.io",
    "humble-store": "Humble Store",
    "fanatical": "Fanatical",
    "indiegala": "IndieGala",
    "other": "Otras Plataformas"
}

# --- PALETAS DE COLORES PARA TEMAS (OSCURO / CLARO) ---
THEMES = {
    "dark": {
        "COLOR_BG": "#1E1E2E",
        "COLOR_BG_CARD": "#2D2D3F",
        "COLOR_BG_DESC": "#232333",
        "COLOR_SIDEBAR": "#171827",
        "COLOR_SIDEBAR_HOVER": "#25263A",
        "COLOR_TEXT_PRIMARY": "#F3F4F6",
        "COLOR_TEXT_SECONDARY": "#9CA3AF",
        "COLOR_TEXT_MUTED": "#D1D5DB",
        "COLOR_ACCENT": "#6366F1",
        "COLOR_ACCENT_HOVER": "#4F46E5",
        "COLOR_ACCENT_LIGHT": "#818CF8",
        "COLOR_SUCCESS": "#10B981",
        "COLOR_SUCCESS_HOVER": "#059669",
        "COLOR_WARNING": "#F59E0B",
        "COLOR_ERROR": "#EF4444",
        "COLOR_BORDER": "#3A3A50",
        "COLOR_HOVER": "#39394D",
    },
    "light": {
        "COLOR_BG": "#D8E4F3",
        "COLOR_BG_CARD": "#C4D5EA",
        "COLOR_BG_DESC": "#B5C9E2",
        "COLOR_SIDEBAR": "#243A5A",
        "COLOR_SIDEBAR_HOVER": "#304D75",
        "COLOR_TEXT_PRIMARY": "#0F1E33",     # Oscurecido: contraste alto (> 10:1)
        "COLOR_TEXT_SECONDARY": "#1E334D",   # Corregido: ratio > 6:1 (cumple WCAG AA)
        "COLOR_TEXT_MUTED": "#2C405C",       # Corregido: ratio > 4.7:1 (cumple WCAG AA)
        "COLOR_ACCENT": "#4356D6",           # Ajustado para lectura nítida sobre azul claro
        "COLOR_ACCENT_HOVER": "#3545B3",
        "COLOR_ACCENT_LIGHT": "#5E70E8",
        "COLOR_SUCCESS": "#0E755D",          # Reforzado contraste
        "COLOR_SUCCESS_HOVER": "#095442",
        "COLOR_WARNING": "#8A5608",          # Reforzado contraste
        "COLOR_ERROR": "#B91C1C",            # Reforzado contraste
        "COLOR_BORDER": "#8EA7C7",
        "COLOR_HOVER": "#AEC2DD",
    }
}

# Paleta predeterminada (Modo Oscuro)
CURRENT_THEME = "dark"
COLOR_BG = THEMES[CURRENT_THEME]["COLOR_BG"]
COLOR_BG_CARD = THEMES[CURRENT_THEME]["COLOR_BG_CARD"]
COLOR_BG_DESC = THEMES[CURRENT_THEME]["COLOR_BG_DESC"]
COLOR_SIDEBAR = THEMES[CURRENT_THEME]["COLOR_SIDEBAR"]
COLOR_SIDEBAR_HOVER = THEMES[CURRENT_THEME]["COLOR_SIDEBAR_HOVER"]
COLOR_TEXT_PRIMARY = THEMES[CURRENT_THEME]["COLOR_TEXT_PRIMARY"]
COLOR_TEXT_SECONDARY = THEMES[CURRENT_THEME]["COLOR_TEXT_SECONDARY"]
COLOR_TEXT_MUTED = THEMES[CURRENT_THEME]["COLOR_TEXT_MUTED"]
COLOR_ACCENT = THEMES[CURRENT_THEME]["COLOR_ACCENT"]
COLOR_ACCENT_HOVER = THEMES[CURRENT_THEME]["COLOR_ACCENT_HOVER"]
COLOR_ACCENT_LIGHT = THEMES[CURRENT_THEME]["COLOR_ACCENT_LIGHT"]
COLOR_SUCCESS = THEMES[CURRENT_THEME]["COLOR_SUCCESS"]
COLOR_SUCCESS_HOVER = THEMES[CURRENT_THEME]["COLOR_SUCCESS_HOVER"]
COLOR_WARNING = THEMES[CURRENT_THEME]["COLOR_WARNING"]
COLOR_ERROR = THEMES[CURRENT_THEME]["COLOR_ERROR"]
COLOR_BORDER = THEMES[CURRENT_THEME]["COLOR_BORDER"]
COLOR_HOVER = THEMES[CURRENT_THEME]["COLOR_HOVER"]

# --- VENTANA Y SPLASH ---
WINDOW_TITLE = "K GAME TRACKER"
WINDOW_SIZE = "1024x680"
THUMBNAIL_SIZE = (192, 108)

SPLASH_CHROMA_KEY = "#FF00FF"
SPLASH_MAX_WIDTH = 400
SPLASH_CORNER_RADIUS = 40

# --- AUDIO ---
AUDIO_PATH = os.path.join(BASE_DIR, "chill.wav")
AUDIO_ENABLED = True
AUDIO_VOLUME_TARGET = 0.05
AUDIO_FADE_IN_DURATION = 3.0

# --- AUTOSTART (Windows) ---
AUTOSTART_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
AUTOSTART_APP_NAME = "KGameTracker"
