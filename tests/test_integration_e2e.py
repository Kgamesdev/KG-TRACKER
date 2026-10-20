import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.paths import get_user_data_dir
from core.storage import guardar_json_atomico, cargar_json_seguro
from core.validators import es_url_segura
from core.tray import enviar_notificacion_windows
from core.network import crear_sesion_http_segura


class TestIntegrationE2E(unittest.TestCase):

    def test_full_application_lifecycle(self):
        """Prueba integrada sin sobrescribir datos reales ni mostrar notificaciones."""
        # 1. Comprobar la ruta de datos de usuario.
        user_dir = get_user_data_dir()
        self.assertTrue(user_dir.exists())

        # 2 y 3. Probar persistencia exclusivamente en archivos temporales.
        with tempfile.TemporaryDirectory(prefix="kgtracker-test-") as tmp:
            settings_file = Path(tmp) / "settings.json"
            reclamados_file = Path(tmp) / "reclamados.json"

            config_test = {
                "idioma": "es",
                "notificaciones_activas": True,
                "modo_animacion": "full",
            }
            self.assertTrue(guardar_json_atomico(str(settings_file), config_test))
            loaded_cfg = cargar_json_seguro(
                str(settings_file), valor_por_defecto={}
            )
            self.assertEqual(loaded_cfg, config_test)

            reclamados_test = [
                {"id": "game-101", "title": "Cyberpunk Free Game"}
            ]
            self.assertTrue(
                guardar_json_atomico(str(reclamados_file), reclamados_test)
            )
            loaded_rec = cargar_json_seguro(
                str(reclamados_file), valor_por_defecto=[]
            )
            self.assertEqual(loaded_rec, reclamados_test)

        # 4. Validaciones de red.
        self.assertTrue(
            es_url_segura("https://store.epicgames.com/p/free-game")
        )
        self.assertFalse(es_url_segura("http://insecure-http-site.com"))

        # 5. La sesión HTTP exige verificación TLS.
        session = crear_sesion_http_segura()
        try:
            self.assertIs(session.verify, True)
        finally:
            session.close()

        # 6. Comprobar que se solicita la notificación sin lanzar un hilo real.
        with patch("core.tray.threading.Thread") as thread_mock:
            enviar_notificacion_windows("E2E Test", "OK")
            thread_mock.assert_called_once()
            thread_mock.return_value.start.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
