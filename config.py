# --- VERSION Y ACTUALIZACIONES ---
APP_VERSION = "0.3.0"
GITHUB_REPO = "Kgamesdev/KG-TRACKER"
GITHUB_RELEASES_URL = f"https://github.com/{GITHUB_REPO}/releases"
GITHUB_API_LATEST_RELEASE = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
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
        "COLOR_BG": "#F1F5F9",
        "COLOR_BG_CARD": "#FFFFFF",
        "COLOR_BG_DESC": "#E2E8F0",
        "COLOR_SIDEBAR": "#E2E8F0",
        "COLOR_SIDEBAR_HOVER": "#CBD5E1",
        "COLOR_TEXT_PRIMARY": "#0F172A",
        "COLOR_TEXT_SECONDARY": "#334155",
        "COLOR_TEXT_MUTED": "#64748B",
        "COLOR_ACCENT": "#4F46E5",
        "COLOR_ACCENT_HOVER": "#4338CA",
        "COLOR_ACCENT_LIGHT": "#6366F1",
        "COLOR_SUCCESS": "#0D9488",
        "COLOR_SUCCESS_HOVER": "#0F766E",
        "COLOR_WARNING": "#F59E0B",
        "COLOR_ERROR": "#DC2626",
        "COLOR_BORDER": "#CBD5E1",
        "COLOR_HOVER": "#F8FAFC",
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
_audio_ogg = os.path.join(BASE_DIR, "assets", "chill.ogg")
_audio_wav = os.path.join(BASE_DIR, "assets", "chill.wav")
AUDIO_PATH = _audio_ogg if os.path.exists(_audio_ogg) else _audio_wav
AUDIO_ENABLED = True
AUDIO_VOLUME_TARGET = 0.05
AUDIO_FADE_IN_DURATION = 3.0

# --- AUTOSTART (Windows) ---
AUTOSTART_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
AUTOSTART_APP_NAME = "KGameTracker"


