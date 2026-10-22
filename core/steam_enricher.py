from core.storage import guardar_json_atomico, cargar_json_seguro
import threading
"""Módulo para enriquecer ofertas con reseñas de la comunidad de Steam."""

import json
import os
import re
import urllib.parse
from PySide6.QtCore import QObject, Signal, QThreadPool, QRunnable
import requests
from core.paths import CACHE_STEAM_FILE as CACHE_FILE

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
    return cargar_json_seguro(CACHE_FILE, valor_por_defecto={})


def _guardar_cache(cache):
    try:
        guardar_json_atomico(CACHE_FILE, cache)
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
        fallback_image_url = candidato.get("tiny_image")

        url_reviews = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
        resp_rev = session.get(url_reviews, headers=headers, timeout=5)
        if resp_rev.status_code != 200:
            return {
                "found": True, "appid": appid, "banner_url": banner_url,
                "fallback_image_url": fallback_image_url, "percent": 0,
            }

        data_rev = resp_rev.json()
        summary = data_rev.get("query_summary", {})
        total_reviews = summary.get("total_reviews", 0)
        total_positive = summary.get("total_positive", 0)
        review_desc = summary.get("review_score_desc", "")

        if total_reviews <= 0:
            return {
                "found": True, "appid": appid, "banner_url": banner_url,
                "fallback_image_url": fallback_image_url, "percent": 0,
            }

        percent = int(round((total_positive / total_reviews) * 100))
        return {
            "found": True,
            "appid": appid,
            "percent": percent,
            "desc_en": review_desc,
            "desc_es": RESENAS_ES.get(review_desc.lower(), review_desc),
            "total_reviews": total_reviews,
            "banner_url": banner_url,
            "fallback_image_url": fallback_image_url,
        }
    except Exception:
        return {"found": False}


class _SteamWorker(QRunnable):
    def __init__(self, titulo, clave, enricher):
        super().__init__()
        self.titulo = titulo
        self.clave = clave
        self.enricher = enricher

    def run(self):
        try:
            with requests.Session() as session:
                datos = self.enricher._obtener_resenas_sincrono(self.titulo, session=session)
        except Exception:
            datos = {"found": False}
        self.enricher.signals.resultado.emit(self.clave, datos, None)


class _SteamSignals(QObject):
    resultado = Signal(str, dict, object)


class SteamEnricher(QObject):
    _instance = None

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self.cache = _cargar_cache()
        self._pendientes = {}
        self.signals = _SteamSignals()
        self.signals.resultado.connect(self._al_emitir_resultado)
        # Las tarjetas no deben saturar el pool global de imágenes y búsquedas.
        self._pool = QThreadPool(self)
        self._pool.setMaxThreadCount(2)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
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
                if cached.get("appid") and "fallback_image_url" not in cached:
                    cached["fallback_image_url"] = f"https://cdn.akamai.steamstatic.com/steam/apps/{cached['appid']}/capsule_sm_120.jpg"
                return cached

        s = session or requests
        res = _consultar_steam_red(s, t_limpio)
        if res.get("found"):
            with self._lock:
                self.cache[clave] = res
                _guardar_cache(self.cache)
        return res

    def obtener_resenas_async(self, titulo: str, callback):
        clave = limpiar_titulo(titulo).lower()
        if not clave:
            callback({"found": False})
            return

        with self._lock:
            cached = self.cache.get(clave)
            if cached:
                datos_cacheados = dict(cached)
                if datos_cacheados.get("appid") and "banner_url" not in datos_cacheados:
                    datos_cacheados["banner_url"] = (
                        f"https://cdn.akamai.steamstatic.com/steam/apps/"
                        f"{datos_cacheados['appid']}/header.jpg"
                    )
                if datos_cacheados.get("appid") and "fallback_image_url" not in datos_cacheados:
                    datos_cacheados["fallback_image_url"] = (
                        f"https://cdn.akamai.steamstatic.com/steam/apps/"
                        f"{datos_cacheados['appid']}/capsule_sm_120.jpg"
                    )
            else:
                datos_cacheados = None
            if datos_cacheados is None:
                callbacks = self._pendientes.setdefault(clave, [])
                callbacks.append(callback)
                if len(callbacks) > 1:
                    return

        if datos_cacheados is not None:
            callback(datos_cacheados)
            return

        worker = _SteamWorker(titulo, clave, self)
        self._pool.start(worker)

    def _al_emitir_resultado(self, clave, datos, _callback=None):
        with self._lock:
            callbacks = self._pendientes.pop(clave, [])
        for callback in callbacks:
            try:
                callback(datos)
            except Exception:
                pass
