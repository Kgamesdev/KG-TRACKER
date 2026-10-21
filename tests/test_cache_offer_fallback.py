import datetime
import unittest

from ui.main_window_games import _fusionar_cache_ofertas


class TestCacheOfferFallback(unittest.TestCase):
    def test_fusiona_por_oferta_y_respeta_vencimientos(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        fresh_cache_time = now - datetime.timedelta(hours=1)
        current = [{
            "title": "Agent A: A puzzle in disguise",
            "store": "Fanatical",
            "end_date": (now + datetime.timedelta(days=1)).isoformat(),
        }]
        cached = [
            {
                "title": "Agent A - un puzle disfrazado",
                "store": "Fanatical",
                "end_date": (now + datetime.timedelta(days=1)).isoformat(),
            },
            {
                "title": "Another active giveaway",
                "store": "Fanatical",
                "end_date": (now + datetime.timedelta(days=2)).isoformat(),
            },
            {
                "title": "Expired giveaway",
                "store": "GOG",
                "end_date": (now - datetime.timedelta(minutes=1)).isoformat(),
            },
            {
                "title": "Unreadable date",
                "store": "GOG",
                "end_date": "not-a-date",
            },
            {"title": "No date, fresh cache", "store": "GOG", "end_date": ""},
        ]

        combined, recovered = _fusionar_cache_ofertas(
            current, cached, now, fresh_cache_time
        )

        self.assertEqual(recovered, 2)
        self.assertEqual(
            [offer["title"] for offer in combined],
            [
                "Agent A: A puzzle in disguise",
                "Another active giveaway",
                "No date, fresh cache",
            ],
        )
        self.assertEqual(combined[1]["_kg_source"], "GamerPower-cache")
        self.assertNotIn("_kg_source", cached[1])

    def test_sin_fecha_solo_acepta_cache_menor_a_12_horas(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        current = []
        stale_cache = [{"title": "Unknown expiry", "store": "GOG"}]

        combined, recovered = _fusionar_cache_ofertas(
            current,
            stale_cache,
            now,
            now - datetime.timedelta(hours=13),
        )

        self.assertEqual(recovered, 0)
        self.assertEqual(combined, [])


if __name__ == "__main__":
    unittest.main()
