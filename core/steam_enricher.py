"""Motor asincrono de Steam con concurrencia x3 y precarga de fondo."""

import os
import re
import json
import time
import queue
import urllib.parse
import requests
from PySide6.QtCore import QObject, Signal, QThread
from config import BASE_DIR

CACHE_FILE = os.path.join(BASE_DIR, "data", "steam_cache.json")

RESENAS_ES = {
    "overwhelmingly positive": "Extremadamente positivas",
    "very positive": "Muy positivas",
    "positive": "Positivas",
    "mostly positive": "Mayormente positivas",
    "mixed": "Variadas",
    "mostly negative": "Mayormente negativas",
    "negative": "Negativas",
    "very negative": "Muy negativas",
    "overwhelmingly negative": "Extremadamente negativas",
}


def _cargar_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _guardar_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    tmp = CACHE_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        os.replace(tmp, CACHE_FILE)
    except Exception:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass


def limpiar_titulo(titulo: str) -> str:
    t = str(titulo or "").strip()
    t = re.sub(r"\s*[\(\[].*?[\)\]]", "", t)
    for sufijo in (" giveaway", " - giveaway", " : giveaway", " free"):
        if t.lower().endswith(sufijo):
            t = t[:-len(sufijo)].strip()
    return " ".join(t.split()).strip()


def _consultar_steam_red(session: requests.Session, titulo_limpio: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "es,en;q=0.9",
    }
    try:
        url_search = f"https://store.steampowered.com/api/storesearch/?term={urllib.parse.quote(titulo_limpio)}&l=spanish&cc=ES"
        resp = session.get(url_search, headers=headers, timeout=5)
        if resp.status_code != 200:
            return {"found": False}

        data = resp.json()
        items = data.get("items", [])
        if not items:
            return {"found": False}

        candidato = items[0]
        appid = candidato.get("id")
        if not appid:
            return {"found": False}

        url_reviews = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
        resp_rev = session.get(url_reviews, headers=headers, timeout=5)
        if resp_rev.status_code != 200:
            return {"found": False}

        data_rev = resp_rev.json()
        summary = data_rev.get("query_summary", {})
        total_reviews = summary.get("total_reviews", 0)
        total_positive = summary.get("total_positive", 0)
        review_desc = summary.get("review_score_desc", "")

        if total_reviews <= 0:
            return {"found": False}

        percent = int(round((total_positive / total_reviews) * 100))
        return {
            "found": True,
            "appid": appid,
            "percent": percent,
            "desc_en": review_desc,
            "desc_es": RESENAS_ES.get(review_desc.lower(), review_desc),
            "total_reviews": total_reviews,
        }
    except Exception:
        return {"found": False}


class _SteamWorkerThread(QThread):
    resultado_signal = Signal(str, dict)

    def __init__(self, cola: queue.Queue):
        super().__init__()
        self.cola = cola
        self._activo = True

    def run(self):
        session = requests.Session()
        while self._activo:
            try:
                item = self.cola.get(timeout=1.0)
            except queue.Empty:
                continue

            titulo_limpio = item
            datos = _consultar_steam_red(session, titulo_limpio)
            self.resultado_signal.emit(titulo_limpio, datos)
            self.cola.task_done()
            time.sleep(0.10)  # Pausa minima optimizada para concurrencia


class SteamEnricher(QObject):
    _instancia = None

    @classmethod
    def get_instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        super().__init__()
        self._cache = _cargar_cache()
        self._pendientes = {}
        self._cola = queue.Queue()

        # Pool de 3 hilos paralelos para acelerar las consultas a Steam
        self._workers = []
        for _ in range(3):
            w = _SteamWorkerThread(self._cola)
            w.resultado_signal.connect(self._al_recibir_resultado)
            w.start()
            self._workers.append(w)

    def obtener_resenas_async(self, titulo_original: str, callback):
        titulo_limpio = limpiar_titulo(titulo_original).lower()
        if not titulo_limpio:
            callback(None)
            return

        if titulo_limpio in self._cache:
            callback(self._cache[titulo_limpio])
            return

        if titulo_limpio in self._pendientes:
            self._pendientes[titulo_limpio].append(callback)
            return

        self._pendientes[titulo_limpio] = [callback]
        self._cola.put(titulo_limpio)

    def precargar_async(self, lista_titulos: list):
        """Precarga en background todos los titulos de las ofertas obtenidas."""
        for tit in lista_titulos:
            if tit:
                self.obtener_resenas_async(tit, lambda _: None)

    def _al_recibir_resultado(self, titulo_limpio: str, datos: dict):
        self._cache[titulo_limpio] = datos
        _guardar_cache(self._cache)

        callbacks = self._pendientes.pop(titulo_limpio, [])
        for cb in callbacks:
            try:
                cb(datos)
            except Exception:
                pass
