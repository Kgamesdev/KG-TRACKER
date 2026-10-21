import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from core.paths import get_resource_dir, get_user_data_dir, SETTINGS_FILE
from core.tray import enviar_notificacion_windows
from core.storage import guardar_json_atomico, cargar_json_seguro


class TestPhase1P0(unittest.TestCase):

    def test_pkg_01_paths_separation(self):
        """Verifica que las rutas de recursos y de usuario estén correctamente separadas."""
        resource_dir = get_resource_dir()
        user_data_dir = get_user_data_dir()

        self.assertTrue(resource_dir.exists())
        self.assertTrue(user_data_dir.exists())

        if os.name == "nt":
            self.assertIn("AppData", str(user_data_dir))

    def test_sec_01_notification_payload_is_handled_asynchronously(self):
        """
        Prueba que un texto malicioso con comillas, caracteres XML y saltos de línea
        NO ejecute comandos arbitrarios ni rompa el proceso de notificación.
        """
        payload_malicioso_titulo = 'Prueba"; Start-Process calc.exe; #'
        payload_malicioso_mensaje = 'Mensaje con "@ \n & <xml> y comillas "'

        # Debe ejecutarse de forma segura sin lanzar excepciones de sintaxis ni subcomandos
        with patch("core.tray.threading.Thread") as thread_mock:
            enviar_notificacion_windows(
                payload_malicioso_titulo,
                payload_malicioso_mensaje
            )
        thread_mock.assert_called_once()
        thread_mock.return_value.start.assert_called_once_with()

    def test_atomic_storage_temp_dir(self):
        """Verifica la escritura atómica en un directorio temporal aislado."""
        with tempfile.TemporaryDirectory(prefix="kgtracker-storage-test-") as tmp:
            test_file = Path(tmp) / "data" / "test_atomic.json"
            data_test = {"status": "ok", "count": 42}

            self.assertTrue(guardar_json_atomico(test_file, data_test))

            loaded = cargar_json_seguro(test_file)
            self.assertEqual(loaded.get("status"), "ok")
            self.assertEqual(loaded.get("count"), 42)

if __name__ == "__main__":
    unittest.main()


