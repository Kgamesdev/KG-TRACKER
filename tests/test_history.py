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


    def test_guardado_atomico_y_rescate_bak(self):
        import tempfile
        import os
        from core.storage import guardar_json_atomico, cargar_json_seguro

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test_reclamados.json")
            datos = {"game:steam|portal": {"title": "Portal", "worth_value": 9.99}}

            # 1. Guardar atómicamente
            self.assertTrue(guardar_json_atomico(test_file, datos))
            self.assertTrue(os.path.exists(test_file))

            # 2. Guardar actualización (debe generar el .bak)
            datos["game:steam|portal 2"] = {"title": "Portal 2", "worth_value": 9.99}
            guardar_json_atomico(test_file, datos)
            self.assertTrue(os.path.exists(f"{test_file}.bak"))

            # 3. Simular corrupción del archivo principal
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("{corrupted_json: incomplete")

            # 4. cargar_json_seguro debe rescatar los datos desde el .bak automáticamente
            rescatados = cargar_json_seguro(test_file, valor_por_defecto={})
            self.assertIn("game:steam|portal", rescatados)

if __name__ == "__main__":
    unittest.main()
