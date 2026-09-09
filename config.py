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

# --- PALETAS DE COLORES PARA TEMAS ---
# Diseño: azul grisáceo de baja luminosidad + acento violeta KG.
# El modo claro evita blanco puro para reducir fatiga visual.
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
        # Azul grisáceo oscuro, inspirado en launchers modernos.
        "COLOR_BG": "#536B99",
        "COLOR_BG_CARD": "#6079A8",
        "COLOR_BG_DESC": "#6E86B2",
        "COLOR_SIDEBAR": "#172744",
        "COLOR_SIDEBAR_HOVER": "#243A61",
        "COLOR_TEXT_PRIMARY": "#F1F5FC",
        "COLOR_TEXT_SECONDARY": "#D4DEEE",
        "COLOR_TEXT_MUTED": "#B9C7DD",
        # El violeta queda reservado para acciones/acento.
        "COLOR_ACCENT": "#665CF0",
        "COLOR_ACCENT_HOVER": "#554AE0",
        "COLOR_ACCENT_LIGHT": "#A7B4FF",
        "COLOR_SUCCESS": "#43C5A0",
        "COLOR_SUCCESS_HOVER": "#2DAF8B",
        "COLOR_WARNING": "#F0B85B",
        "COLOR_ERROR": "#F07A7A",
        "COLOR_BORDER": "#7890BC",
        "COLOR_HOVER": "#6D86B4",
    }
}

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
# Ruta absoluta: si se deja relativa, al lanzar la app desde el Registro
# (autostart) el directorio de trabajo puede no ser el de la app y el
# audio no se encontraría nunca (fallo silencioso, capturado por el
# try/except de _inicializar_audio).
AUDIO_PATH = os.path.join(BASE_DIR, "chill.wav")
AUDIO_ENABLED = True
AUDIO_VOLUME_TARGET = 0.1  # 10%
AUDIO_FADE_IN_DURATION = 3.0  # segundos

# --- AUTOSTART (Windows) ---
AUTOSTART_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
AUTOSTART_APP_NAME = "KGameTracker"
