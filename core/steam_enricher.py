from core.storage import guardar_json_atomico, cargar_json_seguro
import threading
"""Modulo para enriquecer ofertas con resenas de la comunidad de Steam."""

import json
import os
import re
import urllib.parse
from PySide6.QtCore import QObject, Signal, QThreadPool, QRunnable
import requests
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


def _consultar_steam_red(session, titulo_limpio: str) -> dict:
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

        banner_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"

        url_reviews = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
        resp_rev = session.get(url_reviews, headers=headers, timeout=5)
        if resp_rev.status_code != 200:
            return {"found": True, "appid": appid, "banner_url": banner_url, "percent": 0}

        data_rev = resp_rev.json()
        summary = data_rev.get("query_summary", {})
        total_reviews = summary.get("total_reviews", 0)
        total_positive = summary.get("total_positive", 0)
        review_desc = summary.get("review_score_desc", "")

        if total_reviews <= 0:
            return {"found": True, "appid": appid, "banner_url": banner_url, "percent": 0}

        percent = int(round((total_positive / total_reviews) * 100))
        return {
            "found": True,
            "appid": appid,
            "percent": percent,
            "desc_en": review_desc,
            "desc_es": RESENAS_ES.get(review_desc.lower(), review_desc),
            "total_reviews": total_reviews,
            "banner_url": banner_url,
        }
    except Exception:
        return {"found": False}


class _SteamWorker(QRunnable):
    def __init__(self, titulo, callback, enricher):
        super().__init__()
        self.titulo = titulo
        self.callback = callback
        self.enricher = enricher

    def run(self):
        # Crear sesión HTTP local e independiente por hilo para evitar condiciones de carrera
        with requests.Session() as session:
            datos = self.enricher._obtener_resenas_sincrono(self.titulo, session=session)
        self.enricher.signals.resultado.emit(self.titulo, datos, self.callback)


class _SteamSignals(QObject):
    resultado = Signal(str, dict, object)


class SteamEnricher:
    _instance = None

    def __init__(self):
        self._lock = threading.Lock()
        self.cache = _cargar_cache()
        self.signals = _SteamSignals()
        self.signals.resultado.connect(self._al_emitir_resultado)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SteamEnricher()
        return cls._instance

    def _obtener_resenas_sincrono(self, titulo: str, session: requests.Session = None) -> dict:
        t_limpio = limpiar_titulo(titulo)
        if not t_limpio:
            return {"found": False}

        clave = t_limpio.lower()
        with self._lock:
            cached = self.cache.get(clave)
            if cached:
                if cached.get("appid") and "banner_url" not in cached:
                    cached["banner_url"] = f"https://cdn.akamai.steamstatic.com/steam/apps/{cached['appid']}/header.jpg"
                return cached

        s = session or requests
        res = _consultar_steam_red(s, t_limpio)
        if res.get("found"):
            with self._lock:
                self.cache[clave] = res
                _guardar_cache(self.cache)
        return res

    def obtener_resenas_async(self, titulo: str, callback):
        worker = _SteamWorker(titulo, callback, self)
        QThreadPool.globalInstance().start(worker)

    def _al_emitir_resultado(self, titulo, datos, callback):
        if callable(callback):
            try:
                callback(datos)
            except Exception:
                pass
