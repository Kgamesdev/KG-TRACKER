import unittest
from core.ui_settings import AnimationMode, obtener_modo_animacion
from ui.design_system import DARK_PALETTE, LIGHT_PALETTE, SPACING, obtener_paleta


class TestPhase3UX(unittest.TestCase):

    def test_design_tokens_structure(self):
        """Verifica que ambas paletas contengan las claves fundamentales de color."""
        keys_requeridas = [
            "bg_main", "bg_surface", "text_primary", "text_secondary",
            "accent_primary", "accent_cyan", "success", "border_focus"
        ]
        for key in keys_requeridas:
            self.assertIn(key, DARK_PALETTE)
            self.assertIn(key, LIGHT_PALETTE)

    def test_spacing_grid_multiples(self):
        """Verifica que el sistema de espaciado responda al estándar de múltiplos de 8 (o 4 para xs)."""
        self.assertEqual(SPACING["xs"], 4)
        self.assertEqual(SPACING["sm"], 8)
        self.assertEqual(SPACING["md"], 16)
        self.assertEqual(SPACING["lg"], 24)

    def test_animation_mode_enum(self):
        """Verifica la existencia de los 3 modos de animación."""
        modos = [m.value for m in AnimationMode]
        self.assertIn("full", modos)
        self.assertIn("reduced", modos)
        self.assertIn("disabled", modos)


if __name__ == "__main__":
    unittest.main()
