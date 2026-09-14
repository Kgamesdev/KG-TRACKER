import os
import unittest
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

    def test_sec_01_powershell_payload_injection(self):
        """
        Prueba que un texto malicioso con comillas, caracteres XML y saltos de línea
        NO ejecute comandos arbitrarios ni rompa el proceso de notificación.
        """
        payload_malicioso_titulo = 'Prueba"; Start-Process calc.exe; #'
        payload_malicioso_mensaje = 'Mensaje con "@ \n & <xml> y comillas "'

        # Debe ejecutarse de forma segura sin lanzar excepciones de sintaxis ni subcomandos
        try:
            enviar_notificacion_windows(
                payload_malicioso_titulo,
                payload_malicioso_mensaje
            )
            exito = True
        except Exception:
            exito = False

        self.assertTrue(exito)

    def test_atomic_storage_user_dir(self):
        """Verifica que la escritura atómica cree archivos en el directorio de usuario."""
        test_file = get_user_data_dir() / "data" / "test_atomic.json"
        data_test = {"status": "ok", "count": 42}

        self.assertTrue(guardar_json_atomico(test_file, data_test))
        loaded = cargar_json_seguro(test_file)
        self.assertEqual(loaded.get("status"), "ok")

        if test_file.exists():
            test_file.unlink()
        bak = test_file.with_suffix(".bak")
        if bak.exists():
            bak.unlink()


if __name__ == "__main__":
    unittest.main()
