import unittest
from pathlib import Path

from core.paths import get_user_data_dir, SETTINGS_FILE, RECLAMADOS_FILE
from core.storage import guardar_json_atomico, cargar_json_seguro
from core.validators import es_url_segura
from core.tray import enviar_notificacion_windows
from core.network import crear_sesion_http_segura


class TestIntegrationE2E(unittest.TestCase):

    def test_full_application_lifecycle(self):
        """Prueba integrada del flujo de datos, persistencia, red y seguridad."""
        # 1. Configuración y rutas
        user_dir = get_user_data_dir()
        self.assertTrue(user_dir.exists())

        # 2. Persistencia de Ajustes
        config_test = {"idioma": "es", "notificaciones_activas": True, "modo_animacion": "full"}
        self.assertTrue(guardar_json_atomico(SETTINGS_FILE, config_test))
        loaded_cfg = cargar_json_seguro(SETTINGS_FILE, valor_por_defecto={})
        self.assertEqual(loaded_cfg.get("idioma"), "es")

        # 3. Persistencia de Reclamados
        reclamados_test = [{"id": "game-101", "title": "Cyberpunk Free Game"}]
        self.assertTrue(guardar_json_atomico(RECLAMADOS_FILE, reclamados_test))
        loaded_rec = cargar_json_seguro(RECLAMADOS_FILE, valor_por_defecto=[])
        self.assertEqual(len(loaded_rec), 1)

        # 4. Validaciones de Red
        self.assertTrue(es_url_segura("https://store.epicgames.com/p/free-game"))
        self.assertFalse(es_url_segura("http://insecure-http-site.com"))

        # 5. Sesión HTTP Segura
        session = crear_sesion_http_segura()
        self.assertTrue(session.verify)

        # 6. Notificación Nativa Segura
        self.assertTrue(isinstance(enviar_notificacion_windows("E2E Test", "OK"), type(None)))


if __name__ == "__main__":
    unittest.main()
