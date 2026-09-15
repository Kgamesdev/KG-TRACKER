"""Motor de traducción asíncrono para KG Tracker con concurrencia controlada y precarga."""

from core.storage import guardar_json_atomico, cargar_json_seguro             
import threading
import os
import json
import html
import hashlib
import time
import queue
import urllib.parse
import requests
from PySide6.QtCore import QObject, Signal, QThread
from core.paths import CACHE_TRANSLATIONS_FILE as CACHE_FILE


def _cargar_cache():
    return cargar_json_seguro(CACHE_FILE, valor_por_defecto={})


def _guardar_cache(cache):
    try:
        guardar_json_atomico(CACHE_FILE, cache)
    except Exception:
        pass


def _consultar_traduccion_red(session: requests.Session, texto: str, target_lang: str) -> str:
    # Sanitizar target_lang a formato ISO (ej: 'es_ES' o 'es-ES' -> 'es')
    target_lang = str(target_lang or "es").split("_")[0].split("-")[0].lower()

    # 1. API Directa de Google (JSON)
    try:
        url_google = (
            f"https://translate.googleapis.com/translate_a/single?"
            f"client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(texto)}"
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        resp = session.get(url_google, headers=headers, timeout=4)
        if resp.status_code == 200:
            resp.encoding = "utf-8"
            data = resp.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                resultado = "".join([frase[0] for frase in data[0] if frase and len(frase) > 0 and frase[0]])
                if resultado and resultado.strip().lower() != texto.strip().lower():
                    return html.unescape(resultado).strip()
    except Exception:
        pass

    # 2. Respaldo MyMemory API
    try:
        url_mm = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(texto[:400])}&langpair=en|{target_lang}"
        headers_mm = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp_mm = session.get(url_mm, headers=headers_mm, timeout=4)
        if resp_mm.status_code == 200:
            resp_mm.encoding = "utf-8"
            data_mm = resp_mm.json()
            res_mm = data_mm.get("responseData", {}).get("translatedText", "")
            if (
                res_mm 
                and "MYMEMORY WARNING" not in res_mm.upper() 
                and "INVALID TARGET" not in res_mm.upper() 
                and res_mm.lower() != texto.lower()
            ):
                return html.unescape(res_mm).strip()
    except Exception:
        pass

    return texto


class _TranslationWorkerThread(QThread):
    traducido_signal = Signal(str, str, str)

    def __init__(self, cola: queue.Queue):
        super().__init__()
        self.cola = cola
        self._activo = True

    def stop(self):
        self._activo = False

    def run(self):
        session = requests.Session()
        while self._activo:
            try:
                item = self.cola.get(timeout=0.2)
            except queue.Empty:
                continue

            if not self._activo or item is None:
                self.cola.task_done()
                break

            clave, texto, target_lang = item
            traducido = _consultar_traduccion_red(session, texto, target_lang)
            if self._activo:
                self.traducido_signal.emit(clave, texto, traducido)
            self.cola.task_done()
            time.sleep(0.2)


class GameTranslator(QObject):
    _instancia = None

    @classmethod
    def get_instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._cache = _cargar_cache()
        self._pendientes = {}
        self._cola = queue.Queue()

        self._workers = []
        for _ in range(2):
            w = _TranslationWorkerThread(self._cola)
            w.traducido_signal.connect(self._al_terminar_traduccion)
            w.start()
            self._workers.append(w)

    def _generar_clave(self, texto: str, target_lang: str) -> str:
        h = hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()[:16]
        return f"{target_lang}:{h}"

    def traducir_async(self, texto: str, target_lang: str, callback):
        texto_limpio = " ".join(str(texto or "").split())
        lang_normalizado = str(target_lang or "es").split("_")[0].split("-")[0].lower()

        if not texto_limpio or lang_normalizado == "en":
            callback(texto_limpio)
            return

        clave = self._generar_clave(texto_limpio, lang_normalizado)

        with self._lock:
            if clave in self._cache and self._cache[clave].lower() != texto_limpio.lower():
                callback(self._cache[clave])
                return

            if clave in self._pendientes:
                self._pendientes[clave].append(callback)
                return

            self._pendientes[clave] = [callback]
        self._cola.put((clave, texto_limpio, lang_normalizado))

    def precargar_async(self, lista_textos: list, target_lang: str):
        lang_normalizado = str(target_lang or "es").split("_")[0].split("-")[0].lower()
        if lang_normalizado == "en":
            return
        for t in lista_textos:
            if t:
                self.traducir_async(t, lang_normalizado, lambda _: None)

    def _al_terminar_traduccion(self, clave: str, texto_orig: str, traducido: str):
        callbacks = []
        with self._lock:
            if traducido and traducido.lower() != texto_orig.lower():
                self._cache[clave] = traducido
                _guardar_cache(self._cache)

            callbacks = self._pendientes.pop(clave, [])

        for cb in callbacks:
            try:
                cb(traducido)
            except Exception:
                pass

    def detener(self):
        for w in self._workers:
            w.stop()
        for _ in self._workers:
            self._cola.put(None)
        for w in self._workers:
            w.quit()
            w.wait(250)
        self._workers.clear()