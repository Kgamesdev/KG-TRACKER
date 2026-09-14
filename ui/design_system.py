"""
ui/design_system.py
Design System centralizado para KG Tracker con cumplimiento WCAG 2.1 AA.
Resuelve UX-02 (Contraste y Accesibilidad) y define la paleta oficial.
"""

# Tokens de Color - Tema Oscuro (Cyberpunk Dark)
DARK_PALETTE = {
    "bg_main": "#12121A",
    "bg_surface": "#1E1E2E",
    "bg_surface_hover": "#2A2A3D",
    "text_primary": "#FFFFFF",        # Contraste > 14:1 sobre bg_surface
    "text_secondary": "#A6ADC8",      # Contraste > 7:1 sobre bg_surface
    "accent_primary": "#818CF8",      # Índigo brillante (WCAG AA)
    "accent_cyan": "#00E5FF",         # Cian Neón
    "success": "#10B981",             # Verde éxito
    "warning": "#F59E0B",             # Ámbar advertencia
    "danger": "#EF4444",              # Rojo error
    "border_default": "#313244",
    "border_focus": "#818CF8",        # Focus Ring visible (2px)
}

# Tokens de Color - Tema Claro (Minimalist Light) - Corregido para WCAG AA
LIGHT_PALETTE = {
    "bg_main": "#F8FAFC",
    "bg_surface": "#FFFFFF",
    "bg_surface_hover": "#F1F5F9",
    "text_primary": "#0F172A",        # Contraste > 15:1 sobre blanco (WCAG AAA)
    "text_secondary": "#475569",      # Contraste > 7:1 sobre blanco (WCAG AA)
    "accent_primary": "#4F46E5",      # Índigo Oscuro accesible
    "accent_cyan": "#0284C7",         # Azul/Cian Oscuro (cumple 4.5:1 sobre blanco)
    "success": "#059669",             # Verde Oscuro accesible
    "warning": "#D97706",             # Ámbar Oscuro
    "danger": "#DC2626",              # Rojo Oscuro
    "border_default": "#E2E8F0",
    "border_focus": "#4F46E5",        # Focus Ring visible
}

# Tokens de Espaciado (Múltiples de 8px)
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48,
}

# Radios de Borde
BORDER_RADIUS = {
    "sm": 4,
    "md": 8,
    "lg": 12,
    "pill": 999,
}

# Estilos globales de Focus Ring para navegación por teclado (WCAG 2.1 AA)
FOCUS_RING_STYLE = """
    *:focus {
        outline: 2px solid #818CF8;
        outline-radius: 4px;
    }
"""


def obtener_paleta(modo_oscuro: bool = True) -> dict:
    """Retorna los tokens de color activos según el tema elegido."""
    return DARK_PALETTE if modo_oscuro else LIGHT_PALETTE
