"""Pruebas de las correcciones de la auditoría: validador de URLs y descargas seguras.

No requieren Qt ni Windows: solo la biblioteca estándar y requests.
"""

import unittest
from unittest import mock

from core import network
from core.validators import (
    DOMINIOS_GITHUB,
    abrir_url_externa_segura,
    es_url_segura,
)


class TestValidadorUrls(unittest.TestCase):

    def test_rechaza_trampas_de_host(self):
        for url in (
            "https://store.steampowered.com.evil.com/x",
            "https://evil.com/?u=store.steampowered.com",
            "https://store.epicgames.com@evil.com/",
            "https://evilitch.io/",
            "https://notgog.com/",
        ):
            self.assertFalse(es_url_segura(url), url)

    def test_rechaza_credenciales_puertos_y_control(self):
        for url in (
            "https://user@store.epicgames.com/",
            "https://user:pass@store.epicgames.com/",
            "https://gog.com:444/x",
            "https://gog.com/x\r\nSet-Cookie: a=b",
            "https://gog.com/a b",
            "file:///C:/Windows/System32/calc.exe",
            "javascript:alert(1)",
            "",
            None,
        ):
            self.assertFalse(es_url_segura(url), repr(url))

    def test_acepta_tiendas_y_puerto_443(self):
        self.assertTrue(es_url_segura("https://store.steampowered.com/app/1/"))
        self.assertTrue(es_url_segura("https://gog.com:443/game/x"))
        self.assertTrue(es_url_segura("https://www.gamerpower.com/open/abc"))

    def test_lista_github_para_actualizaciones(self):
        url = "https://github.com/Kgamesdev/KG-TRACKER/releases/tag/v0.3.2"
        self.assertTrue(es_url_segura(url, DOMINIOS_GITHUB))
        self.assertFalse(es_url_segura(url))  # no es una tienda
        self.assertFalse(es_url_segura("https://github.com.evil.com/x", DOMINIOS_GITHUB))

    def test_abrir_solo_si_es_segura(self):
        with mock.patch("core.validators.webbrowser") as wb:
            self.assertFalse(abrir_url_externa_segura("file:///C:/x.exe"))
            wb.open.assert_not_called()
            self.assertTrue(abrir_url_externa_segura("https://store.epicgames.com/p/x"))
            wb.open.assert_called_once()
            self.assertTrue(abrir_url_externa_segura("https://ko-fi.com/x", nueva_pestana=True))
            wb.open_new_tab.assert_called_once()


class _Resp:
    def __init__(self, status=200, headers=None, chunks=(b"data",)):
        self.status_code = status
        self.headers = headers or {}
        self._chunks = chunks

    def iter_content(self, chunk_size=8192):
        yield from self._chunks

    def close(self):
        pass


def _sesion_falsa(respuestas):
    sesion = mock.MagicMock()
    sesion.__enter__.return_value = sesion
    sesion.__exit__.return_value = False
    sesion.get.side_effect = list(respuestas)
    return sesion


class TestDescargaSegura(unittest.TestCase):

    def _descargar(self, respuestas, **kw):
        sesion = _sesion_falsa(respuestas)
        with mock.patch.object(network, "crear_sesion_http_segura", return_value=sesion):
            return network.descargar_contenido_seguro("https://cdn.example.com/a.png", **kw), sesion

    def test_descarga_normal(self):
        datos, _ = self._descargar([_Resp(chunks=(b"abc", b"def"))])
        self.assertEqual(datos, b"abcdef")

    def test_redireccion_https_se_sigue(self):
        datos, sesion = self._descargar([
            _Resp(302, {"Location": "https://cdn2.example.com/b.png"}),
            _Resp(chunks=(b"ok",)),
        ])
        self.assertEqual(datos, b"ok")
        self.assertEqual(sesion.get.call_count, 2)

    def test_redireccion_a_http_se_bloquea(self):
        datos, _ = self._descargar([_Resp(302, {"Location": "http://evil.example.com/x.png"})])
        self.assertIsNone(datos)

    def test_bucle_de_redirecciones(self):
        redir = _Resp(302, {"Location": "https://cdn.example.com/a.png"})
        datos, _ = self._descargar([redir] * (network.MAX_REDIRECTS + 1))
        self.assertIsNone(datos)

    def test_limite_de_tamano(self):
        datos, _ = self._descargar([_Resp(headers={"Content-Length": "999999"})], max_size=1000)
        self.assertIsNone(datos)
        datos, _ = self._descargar([_Resp(chunks=(b"x" * 600, b"x" * 600))], max_size=1000)
        self.assertIsNone(datos)

    def test_rechaza_esquemas_no_https(self):
        for url in ("http://example.com/a.png", "ftp://example.com/a.png", "invalid", "", None):
            self.assertIsNone(network.descargar_contenido_seguro(url), repr(url))


if __name__ == "__main__":
    unittest.main()
