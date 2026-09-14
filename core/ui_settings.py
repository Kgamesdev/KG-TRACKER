"""
core/ui_settings.py
Gestor global de preferencias visuales, animaciones (Reduced Motion) y High DPI.
Resuelve UX-01 y UX-03 para accesibilidad y rendimiento.
"""

from enum import Enum
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from core.paths import SETTINGS_FILE
from core.storage import cargar_json_seguro


class AnimationMode(Enum):
    FULL = "full"         # Todas las animaciones y efectos neón activos
    REDUCED = "reduced"   # Solo transiciones esenciales, sin loops continuos
    DISABLED = "disabled" # 0 animaciones, cambios de estado instantáneos


def obtener_modo_animacion() -> AnimationMode:
    """Retorna el modo de animación configurado por el usuario en settings.json."""
    if SETTINGS_FILE.exists():
        cfg = cargar_json_seguro(SETTINGS_FILE, valor_por_defecto={})
        modo_str = str(cfg.get("modo_animacion", "full")).lower()
        if modo_str == "reduced":
            return AnimationMode.REDUCED
        elif modo_str == "disabled":
            return AnimationMode.DISABLED
    return AnimationMode.FULL


def configurar_high_dpi():
    """Configura el soporte de escalado High DPI para pantallas 1080p, 2K y 4K (UX-03)."""
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
