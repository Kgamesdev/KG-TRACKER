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

    def test_actualizar_textos_idioma_incluye_volumen(self):
        from ui.main_window_helpers import _actualizar_textos_idioma
        mock_win = MagicMock()
        mock_win.volume_label = MagicMock()
        mock_win.btn_actualizar = MagicMock()
        mock_win.btn_reclamados = MagicMock()
        mock_win.status_pill = MagicMock()
        mock_win.juegos_cache_global = []
        mock_win.reclamados = {}
        mock_win._esta_reclamado = MagicMock(return_value=False)

        _actualizar_textos_idioma(mock_win)
        mock_win.volume_label.setText.assert_called()
        mock_win.btn_actualizar.setText.assert_called()

    def test_animacion_ahorro_se_pausa_al_ocultar(self):
        from PySide6.QtWidgets import QApplication
        import sys
        app = QApplication.instance() or QApplication(sys.argv)

        from ui.components.game_card import RoundedButton
        from PySide6.QtCore import QVariantAnimation

        btn = RoundedButton(text="$ AHORRADO : 50.00")
        btn.show()
        self.assertEqual(btn._anim.state(), QVariantAnimation.State.Running)

        btn.hide()
        self.assertNotEqual(btn._anim.state(), QVariantAnimation.State.Running)

        btn.show()
        self.assertEqual(btn._anim.state(), QVariantAnimation.State.Running)
        btn.deleteLater()

    def test_parser_itch_robusto_con_tags_anidados(self):
        import re, html, urllib.parse
        chunk = """
        <div class="game_title"><a href="/games/retro-quest"><b>Retro</b> <span>Quest</span></a></div>
        <img data-lazy_src="//img.itch.zone/thumb.png" />
        <div class="game_text">Awesome <i>indie</i> game</div>
        """
        title_m = re.search(r'<div class="game_title">\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', chunk, re.DOTALL)
        self.assertIsNotNone(title_m)
        url_juego = urllib.parse.urljoin("https://itch.io", title_m.group(1).strip())
        titulo = html.unescape(re.sub(r'<[^>]+>', '', title_m.group(2))).strip()

        self.assertEqual(url_juego, "https://itch.io/games/retro-quest")
        self.assertEqual(titulo, "Retro Quest")

    def test_scrapers_aceptan_y_usan_sesion_http(self):
        import requests
        from unittest.mock import MagicMock
        from core.scrapers.store_scrapers import (
            obtener_epic_directo,
            obtener_steam_directo,
            obtener_itch_directo,
            obtener_gog_directo,
        )

        mock_session = MagicMock(spec=requests.Session)
        mock_resp = MagicMock()
        mock_resp.status_code = 500  # Respuesta no-200 para retorno ágil
        mock_session.get.return_value = mock_resp

        self.assertEqual(obtener_epic_directo(session=mock_session), [])
        self.assertEqual(obtener_steam_directo(session=mock_session), [])
        self.assertEqual(obtener_itch_directo(session=mock_session), [])
        self.assertEqual(obtener_gog_directo(session=mock_session), [])
        self.assertEqual(mock_session.get.call_count, 5)

    def test_gog_usa_ruta_alternativa_si_falla_el_catalogo(self):
        from unittest.mock import MagicMock
        import requests
        from core.scrapers.store_scrapers import obtener_gog_directo

        session = MagicMock(spec=requests.Session)
        catalogo_caido = MagicMock(status_code=500)
        web_gog = MagicMock(status_code=200)
        web_gog.json.return_value = {
            "products": [{
                "id": 123,
                "title": "Juego gratis",
                "slug": "juego-gratis",
                "price": {
                    "finalMoney": {"amount": "0"},
                    "baseMoney": {"amount": "12.99"},
                },
            }]
        }
        session.get.side_effect = [catalogo_caido, web_gog]

        ofertas = obtener_gog_directo(session=session)

        self.assertEqual(len(ofertas), 1)
        self.assertEqual(ofertas[0]["store"], "GOG")
        self.assertEqual(ofertas[0]["title"], "Juego gratis")
        self.assertEqual(ofertas[0]["worth_value"], 12.99)
        self.assertEqual(session.get.call_count, 2)

    def test_amazon_prime_lee_ofertas_publicas_y_mantiene_tienda_de_canje(self):
        from unittest.mock import MagicMock
        import datetime
        import requests
        from core.scrapers.store_scrapers import obtener_amazon_prime_directo

        now = datetime.datetime.now(datetime.timezone.utc).date()
        month = now.strftime("%B")
        session = MagicMock(spec=requests.Session)
        response = MagicMock(status_code=200)
        response.text = (
            '<ul><li><span>Juego de prueba</span> (' + month + ' 1, Epic Games Store)</li></ul>'
        )
        session.get.return_value = response

        offers = obtener_amazon_prime_directo(session=session)

        self.assertEqual(len(offers), 1)
        self.assertEqual(offers[0]["title"], "Juego de prueba")
        self.assertEqual(offers[0]["store"], "Amazon Prime")
        self.assertIn("Epic Games Store", offers[0]["platforms"])
        self.assertEqual(offers[0]["open_giveaway_url"], "https://luna.amazon.com/claims")

    def test_amazon_prime_asocia_enlace_individual_por_titulo(self):
        from unittest.mock import MagicMock
        import datetime
        import json
        import requests
        from core.scrapers.store_scrapers import obtener_amazon_prime_directo

        month = datetime.datetime.now(datetime.timezone.utc).strftime("%B")
        article = MagicMock(status_code=200)
        article.text = f"<ul><li>The Da Vinci Cryptex ({month} 1, Legacy Games Code)</li></ul>"
        index = MagicMock(status_code=200)
        index.text = (
            '<script type="application/ld+json">'
            + json.dumps({"@type": "ListItem", "name": "The Da Vinci Cryptex", "url":
                "https://luna.amazon.com/claims/the-da-vinci-cryptex-legacy/dp/amzn1.pg.item.abc"})
            + "</script>"
        )
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = [article, article, index]

        offers = obtener_amazon_prime_directo(session=session)

        self.assertEqual(len(offers), 1)
        self.assertEqual(
            offers[0]["open_giveaway_url"],
            "https://luna.amazon.com/claims/the-da-vinci-cryptex-legacy/dp/amzn1.pg.item.abc",
        )

    def test_ofertas_amazon_con_url_comun_no_se_eliminan_entre_si(self):
        from types import SimpleNamespace
        from ui.main_window_games import _finalizar_busqueda, _asignar_tienda

        window = SimpleNamespace(
            _asignar_tienda=lambda game: _asignar_tienda(None, game),
            _clave_juego=lambda game: game["title"],
            _valor_juego=lambda game: 0,
            _parsear_valor_juego=lambda value: 0,
            _guardar_reclamados=lambda: None,
            _actualizar_contador_ahorrado=lambda: None,
            _esta_reclamado=lambda game: False,
            actualizar_insignias=lambda counts: None,
            _detener_animacion_busqueda=lambda: None,
            _set_status=lambda *args: None,
            _actualizar_visibilidad_atras=lambda: None,
            _actualizar_vista_juegos=lambda: None,
            reclamados={},
            juegos_cache_global=[],
            mostrando_reclamados=False,
        )
        offers = [
            {"title": title, "type": "Game", "store": "Amazon Prime",
             "platforms": "PC, Amazon Prime — Epic Games Store",
             "open_giveaway_url": "https://luna.amazon.com/claims"}
            for title in ("Juego Prime A", "Juego Prime B")
        ]

        _finalizar_busqueda(window, offers, 0)

        self.assertEqual(len(window.juegos_cache_global), 2)

    def test_fanatical_incluye_solo_promocion_gratis_activa(self):
        from unittest.mock import MagicMock
        import datetime
        import requests
        from core.scrapers.store_scrapers import obtener_fanatical_directo

        now = datetime.datetime.now(datetime.timezone.utc)
        day_before = (now - datetime.timedelta(days=1)).strftime("%d %B %Y")
        day_after = (now + datetime.timedelta(days=1)).strftime("%d %B %Y")
        terms = MagicMock(status_code=200)
        terms.text = (
            "<h2>Test Game Free Game Giveaway - Terms &amp; Conditions</h2>"
            f"<p>Promotion: Get Test Game for free! Date of promotion: {day_before}, 10:00 AM GMT. "
            f"End: {day_after}, 11:59 PM GMT</p>"
        )
        product = MagicMock(status_code=200)
        product.text = '<meta property="og:image" content="https://cdn.fanatical.com/test.png"><p>Get this free game giveaway</p>'
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = [terms, product]

        offers = obtener_fanatical_directo(session=session)

        self.assertEqual(len(offers), 1)
        self.assertEqual(offers[0]["title"], "Test Game")
        self.assertEqual(offers[0]["store"], "Fanatical")
        self.assertEqual(offers[0]["open_giveaway_url"], "https://www.fanatical.com/en/game/test-game")

    def test_fanatical_ignora_promocion_caducada(self):
        from unittest.mock import MagicMock
        import datetime
        import requests
        from core.scrapers.store_scrapers import obtener_fanatical_directo

        yesterday = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime("%d %B %Y")
        terms = MagicMock(status_code=200)
        terms.text = (
            "<h2>Old Game Free Game Giveaway - Terms &amp; Conditions</h2>"
            f"<p>Promotion: Get Old Game for free! Date of promotion: {yesterday}, 10:00 AM GMT. "
            f"End: {yesterday}, 11:59 PM GMT</p>"
        )
        session = MagicMock(spec=requests.Session)
        session.get.return_value = terms

        self.assertEqual(obtener_fanatical_directo(session=session), [])
        self.assertEqual(session.get.call_count, 1)

    def test_i18n_fallback_clave_inexistente(self):
        from core.i18n import t
        clave_rara = "clave_inexistente_de_prueba_xyz_999"
        self.assertEqual(t(clave_rara), clave_rara)

    def test_steam_enricher_respuesta_malformada(self):
        from unittest.mock import MagicMock
        from core.steam_enricher import SteamEnricher
        enricher = SteamEnricher()
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"bad_schema": True}
        mock_session.get.return_value = mock_resp

        res = enricher._obtener_resenas_sincrono("Juego Inexistente", session=mock_session)
        self.assertIsInstance(res, dict)

    def test_translator_fallback_red_mock(self):
        from unittest.mock import MagicMock
        from core.translator import _consultar_traduccion_red
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_session.get.return_value = mock_resp

        res = _consultar_traduccion_red(mock_session, "Sample Text", "es")
        self.assertEqual(res, "Sample Text")

    def test_translator_detener_conserva_worker_hasta_que_termine(self):
        import threading
        from core.translator import GameTranslator

        espera_iniciada = threading.Event()
        permitir_terminar = threading.Event()

        class WorkerLento:
            def __init__(self):
                self.running = True
                self.stopped = False
                self.quit_called = False

            def stop(self):
                self.stopped = True

            def isRunning(self):
                return self.running

            def wait(self):
                espera_iniciada.set()
                permitir_terminar.wait(timeout=2)
                self.running = False
                return True

            def quit(self):
                self.quit_called = True

        translator = GameTranslator.__new__(GameTranslator)
        worker = WorkerLento()
        translator._workers = [worker]
        closer = threading.Thread(target=translator.detener)
        closer.start()

        try:
            self.assertTrue(espera_iniciada.wait(timeout=1))
            self.assertTrue(worker.stopped)
            self.assertFalse(worker.quit_called)
            self.assertEqual(translator._workers, [worker])
        finally:
            permitir_terminar.set()
            closer.join(timeout=2)

        self.assertFalse(closer.is_alive())
        self.assertEqual(translator._workers, [])

    def test_translator_cierre_espera_peticion_http_en_curso(self):
        import threading
        from unittest.mock import patch
        from core.translator import GameTranslator

        peticion_iniciada = threading.Event()
        permitir_respuesta = threading.Event()
        cierre_terminado = threading.Event()

        def respuesta_lenta(*_args, **_kwargs):
            peticion_iniciada.set()
            permitir_respuesta.wait(timeout=3)
            return "Traducción de prueba"

        translator = GameTranslator()
        with patch("core.translator._consultar_traduccion_red", side_effect=respuesta_lenta):
            translator._cola.put(("clave", "Slow response", "es"))
            self.assertTrue(peticion_iniciada.wait(timeout=1))

            closer = threading.Thread(
                target=lambda: (translator.detener(), cierre_terminado.set())
            )
            closer.start()
            try:
                self.assertFalse(cierre_terminado.wait(timeout=0.25))
                self.assertEqual(len(translator._workers), 2)
            finally:
                permitir_respuesta.set()
                closer.join(timeout=2)

        self.assertTrue(cierre_terminado.is_set())
        self.assertFalse(closer.is_alive())
        self.assertEqual(translator._workers, [])

if __name__ == "__main__":
    unittest.main()
