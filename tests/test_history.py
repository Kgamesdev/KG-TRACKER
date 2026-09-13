import unittest
from unittest.mock import MagicMock

class TestHistory(unittest.TestCase):
    def test_parsear_valor_juego(self):
        from ui.main_window_history import _parsear_valor_juego
        mock_self = MagicMock()
        self.assertEqual(_parsear_valor_juego(mock_self, "$19.99"), 19.99)
        self.assertEqual(_parsear_valor_juego(mock_self, ".99"), 0.99)
        self.assertEqual(_parsear_valor_juego(mock_self, "14,99 €"), 14.99)
        self.assertEqual(_parsear_valor_juego(mock_self, "Free"), 0.0)
        self.assertEqual(_parsear_valor_juego(mock_self, None), 0.0)
        self.assertEqual(_parsear_valor_juego(mock_self, "N/A"), 0.0)
        self.assertEqual(_parsear_valor_juego(mock_self, 50), 50.0)

    def test_normalizar_titulo_clave(self):
        from ui.main_window_history import _normalizar_titulo_clave
        self.assertEqual(_normalizar_titulo_clave("The Fall (Epic Games)"), "the fall")
        self.assertEqual(_normalizar_titulo_clave("The Fall - Giveaway"), "the fall")
        self.assertEqual(_normalizar_titulo_clave("The Fall [Epic]"), "the fall")
        self.assertEqual(_normalizar_titulo_clave("Half-Life - Free Steam Key"), "half life")
        self.assertEqual(_normalizar_titulo_clave("Half-Life"), "half life")

if __name__ == "__main__":
    unittest.main()
