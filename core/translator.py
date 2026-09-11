"""Motor de traduccion asincrono para KG Tracker con concurrencia controlada y precarga."""

import os
import json
import html
import re
import hashlib
import time
import queue
import urllib.parse
import requests
from PySide6.QtCore import QObject, Signal, QThread
from config import BASE_DIR

CACHE_FILE = os.path.join(BASE_DIR, "data", "translations_cache.json")


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


def _consultar_traduccion_red(session: requests.Session, texto: str, target_lang: str) -> str:
    # 1. Google Translate Mobile Web Endpoint (100% publico)
    try:
        url_google = f"https://translate.google.com/m?sl=auto&tl={target_lang}&q={urllib.parse.quote(texto)}"
        headers_mobile = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        resp = session.get(url_google, headers=headers_mobile, timeout=5)
        if resp.status_code == 200:
            m = re.search(r'(?s)class="(?:result-container|t0)">(.*?)<', resp.text)
            if m:
                resultado = html.unescape(m.group(1)).strip()
                if resultado and resultado.lower() != texto.lower():
                    return resultado
    except Exception:
        pass

    # 2. Respaldo MyMemory API
    try:
        url_mm = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(texto[:450])}&langpair=en|{target_lang}"
        headers_mm = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp_mm = session.get(url_mm, headers=headers_mm, timeout=5)
        if resp_mm.status_code == 200:
            data_mm = resp_mm.json()
            res_mm = data_mm.get("responseData", {}).get("translatedText", "")
            if res_mm and "MYMEMORY WARNING" not in res_mm.upper() and res_mm.lower() != texto.lower():
                return html.unescape(res_mm).strip()
    except Exception:
        pass

    return texto


class _TranslationWorkerThread(QThread):
    traducido_signal = Signal(str, str, str)  # clave, texto_orig, texto_traducido

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

            clave, texto, target_lang = item
            traducido = _consultar_traduccion_red(session, texto, target_lang)
            self.traducido_signal.emit(clave, texto, traducido)
            self.cola.task_done()
            time.sleep(0.08)  # Pausa minima optimizada para concurrencia


class GameTranslator(QObject):
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

        # Pool de 3 hilos paralelos para acelerar la velocidad x3
        self._workers = []
        for _ in range(3):
            w = _TranslationWorkerThread(self._cola)
            w.traducido_signal.connect(self._al_terminar_traduccion)
            w.start()
            self._workers.append(w)

    def _generar_clave(self, texto: str, target_lang: str) -> str:
        h = hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()[:16]
        return f"{target_lang}:{h}"

    def traducir_async(self, texto: str, target_lang: str, callback):
        texto_limpio = " ".join(str(texto or "").split())
        if not texto_limpio or target_lang == "en":
            callback(texto_limpio)
            return

        clave = self._generar_clave(texto_limpio, target_lang)

        if clave in self._cache and self._cache[clave].lower() != texto_limpio.lower():
            callback(self._cache[clave])
            return

        if clave in self._pendientes:
            self._pendientes[clave].append(callback)
            return

        self._pendientes[clave] = [callback]
        self._cola.put((clave, texto_limpio, target_lang))

    def precargar_async(self, lista_textos: list, target_lang: str):
        """Permite precargar de forma masiva en segundo plano para que esten listos de antemano."""
        if target_lang == "en":
            return
        for t in lista_textos:
            if t:
                self.traducir_async(t, target_lang, lambda _: None)

    def _al_terminar_traduccion(self, clave: str, texto_orig: str, traducido: str):
        if traducido and traducido.lower() != texto_orig.lower():
            self._cache[clave] = traducido
            _guardar_cache(self._cache)

        callbacks = self._pendientes.pop(clave, [])
        for cb in callbacks:
            try:
                cb(traducido)
            except Exception:
                pass
