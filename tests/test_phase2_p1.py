import unittest
from core.validators import es_url_segura, abrir_url_externa_segura
from core.network import descargar_contenido_seguro


class TestPhase2P1(unittest.TestCase):

    def test_sec_02_url_validator_allowed_stores(self):
        """Verifica que las tiendas oficiales permitidas pasen la validación."""
        valid_urls = [
            "https://store.steampowered.com/app/123456/",
            "https://store.epicgames.com/p/game-title",
            "https://www.gog.com/game/title",
            "https://itch.io/games/free",
            "https://ko-fi.com/project",
        ]
        for url in valid_urls:
            self.assertTrue(es_url_segura(url), f"Debería ser válida: {url}")

    def test_sec_02_url_validator_reject_malicious(self):
        """Verifica que URLs inseguras o con esquemas no HTTPS sean rechazadas."""
        invalid_urls = [
            "http://store.steampowered.com/app/123456/",  # HTTP rechazado
            "javascript:alert(1)",                        # Esquema peligroso
            "file:///C:/Windows/System32/cmd.exe",        # Acceso local
            "https://evil-phishing-site.com/steam",       # Dominio no autorizado
            "https://steampowered.com.attacker.com/",     # Subdominio trampa
        ]
        for url in invalid_urls:
            self.assertFalse(es_url_segura(url), f"Debería ser rechazada: {url}")

    def test_sec_03_network_download_limits(self):
        """Verifica que la descarga rechace URLs no HTTPS."""
        self.assertIsNone(descargar_contenido_seguro("http://example.com/image.png"))
        self.assertIsNone(descargar_contenido_seguro("invalid-url"))


if __name__ == "__main__":
    unittest.main()
