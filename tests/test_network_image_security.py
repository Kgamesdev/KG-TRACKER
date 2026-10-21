import unittest
from unittest.mock import MagicMock, patch

from core.network import descargar_contenido_seguro


class TestImageDownloadSecurity(unittest.TestCase):
    def test_rechaza_hosts_no_autorizados_sin_conectar(self):
        with patch("core.network.crear_sesion_http_segura") as crear_sesion:
            self.assertIsNone(
                descargar_contenido_seguro("https://127.0.0.1/private.png")
            )
            self.assertIsNone(
                descargar_contenido_seguro("https://gamerpower.com:8443/image.png")
            )
            crear_sesion.assert_not_called()

    def test_bloquea_redireccion_a_host_no_autorizado(self):
        with patch("core.network.crear_sesion_http_segura") as crear_sesion:
            session = crear_sesion.return_value.__enter__.return_value
            redirect = MagicMock(status_code=302)
            redirect.headers = {"Location": "https://127.0.0.1/private.png"}
            session.get.return_value = redirect

            self.assertIsNone(
                descargar_contenido_seguro("https://www.gamerpower.com/image.png")
            )
            self.assertEqual(session.get.call_count, 1)
            redirect.close.assert_called_once()

    def test_permite_redireccion_entre_cdn_aprobadas(self):
        with patch("core.network.crear_sesion_http_segura") as crear_sesion:
            session = crear_sesion.return_value.__enter__.return_value
            redirect = MagicMock(status_code=301)
            redirect.headers = {
                "Location": "https://shared.akamai.steamstatic.com/image.png"
            }
            image = MagicMock(status_code=200)
            image.headers = {}
            image.iter_content.return_value = [b"image-data"]
            session.get.side_effect = [redirect, image]

            self.assertEqual(
                descargar_contenido_seguro("https://www.gamerpower.com/image.png"),
                b"image-data",
            )
            self.assertEqual(session.get.call_count, 2)
            redirect.close.assert_called_once()
            image.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
