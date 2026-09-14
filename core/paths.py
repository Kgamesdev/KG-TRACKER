"""
core/paths.py
Gestión centralizada de rutas de recursos (solo lectura) y datos de usuario (escritura).
Resuelve el bloqueador PKG-01 para ejecución empaquetada en Windows.
"""

import os
import sys
import shutil
from pathlib import Path


def get_resource_dir() -> Path:
    """Retorna la ruta raíz de recursos (solo lectura). Resuelve PyInstaller _MEIPASS / Dev."""
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_user_data_dir() -> Path:
    """Retorna la ruta escribible para datos del usuario en %LOCALAPPDATA%\KGTracker."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    user_dir = Path(base) / "KGTracker"
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


# --- RUTAS PRINCIPALES ---
RESOURCE_DIR = get_resource_dir()
ASSETS_DIR = RESOURCE_DIR / "assets"

USER_DATA_DIR = get_user_data_dir()
DATA_DIR = USER_DATA_DIR / "data"
CACHE_DIR = USER_DATA_DIR / "cache"
LOGS_DIR = USER_DATA_DIR / "logs"

# Garantizar existencia de directorios escribibles
for path in (DATA_DIR, CACHE_DIR, LOGS_DIR):
    path.mkdir(parents=True, exist_ok=True)

# Archivos de datos y caché
SETTINGS_FILE = DATA_DIR / "settings.json"
RECLAMADOS_FILE = DATA_DIR / "reclamados.json"
CACHE_GIVEAWAYS_FILE = CACHE_DIR / "giveaways_cache.json"
CACHE_STEAM_FILE = CACHE_DIR / "steam_cache.json"
CACHE_TRANSLATIONS_FILE = CACHE_DIR / "translations_cache.json"


def migrar_datos_desarrollo_si_existen():
    """Migra datos locales preexistentes en 'data/' a USER_DATA_DIR en la primera ejecución."""
    dev_data_dir = RESOURCE_DIR / "data"
    if dev_data_dir.exists() and dev_data_dir.is_dir() and dev_data_dir != DATA_DIR:
        for item in dev_data_dir.iterdir():
            target = DATA_DIR / item.name
            if item.is_file() and not target.exists():
                try:
                    shutil.copy2(item, target)
                except Exception as e:
                    print(f"[PATH MIGRATION ERROR] No se pudo migrar {item.name}: {e}")
