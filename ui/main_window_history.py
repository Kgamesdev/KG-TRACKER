"""Histórico de juegos reclamados."""

import json
import os
import re
import webbrowser
from datetime import datetime
from PySide6.QtWidgets import QMessageBox, QLabel, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from config import (
    STORES_MAPPING, COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER,
    COLOR_ACCENT_LIGHT, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR,
)
from ui.game_card import GameCard


def _ruta_reclamados(self):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "reclamados.json")



def _cargar_reclamados(self):
    ruta = self._ruta_reclamados()
    try:
        if not os.path.exists(ruta):
            return {}
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        if not isinstance(datos, dict):
            return {}

        limpios = {}
        for registro in datos.values():
            if not isinstance(registro, dict):
                continue
            titulo = " ".join(str(registro.get("title") or "").lower().split()).strip()
            tienda = " ".join(str(registro.get("store") or "Otras Plataformas").lower().split()).strip()
            for sufijo in (" giveaway", " - giveaway"):
                if titulo.endswith(sufijo):
                    titulo = titulo[:-len(sufijo)].strip()
            clave = f"game:{tienda}|{titulo}"

            if clave not in limpios:
                registro_limpio = dict(registro)
                if "worth_value" not in registro_limpio:
                    registro_limpio["worth_value"] = self._parsear_valor_juego(registro_limpio.get("worth"))
                registro_limpio["key"] = clave
                limpios[clave] = registro_limpio
            else:
                anterior = limpios[clave]
                if str(registro.get("claimed_at", "")) > str(anterior.get("claimed_at", "")):
                    registro_limpio = dict(registro)
                    if "worth_value" not in registro_limpio:
                        registro_limpio["worth_value"] = self._parsear_valor_juego(registro_limpio.get("worth"))
                    registro_limpio["key"] = clave
                    limpios[clave] = registro_limpio

        if limpios != datos:
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    json.dump(limpios, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

                if _scroll_bar and hasattr(_scroll_bar, 'verticalScrollBar'):

                    from PySide6.QtCore import QTimer


                if _scroll_bar and hasattr(_scroll_bar, 'verticalScrollBar'):

                    from PySide6.QtCore import QTimer

        return limpios
    except Exception:
        return {}



def _parsear_valor_juego(self, valor):
    if valor is None:
        return 0.0
    if isinstance(valor, (int, float)):
        return max(0.0, float(valor))
    texto = str(valor).strip()
    if not texto or texto.upper() in {"N/A", "NA", "NONE", "NULL", "FREE"}:
        return 0.0
    limpio = re.sub(r"[^0-9,.-]", "", texto)
    if not limpio:
        return 0.0
    if "," in limpio and "." in limpio:
        if limpio.rfind(",") > limpio.rfind("."):
            limpio = limpio.replace(".", "").replace(",", ".")
        else:
            limpio = limpio.replace(",", "")
    elif "," in limpio:
        partes = limpio.split(",")
        if len(partes[-1]) in (1, 2):
            limpio = "".join(partes[:-1]) + "." + partes[-1]
        else:
            limpio = limpio.replace(",", "")
    try:
        return max(0.0, float(limpio))
    except (TypeError, ValueError):
        return 0.0



def _valor_juego(self, juego):
    if not isinstance(juego, dict):
        return 0.0
    return self._parsear_valor_juego(juego.get("worth_value", juego.get("worth")))



def _dinero_ahorrado(self):
    total = 0.0
    for registro in self.reclamados.values():
        if isinstance(registro, dict):
            total += self._parsear_valor_juego(
                registro.get("worth_value", registro.get("worth"))
            )
    return total



def _actualizar_contador_ahorrado(self):
    if not hasattr(self, "ahorro_pill"):
        return
    total = self._dinero_ahorrado()
    self.ahorro_pill.setText(f"$ AHORRADO : {total:,.2f}")



def _guardar_reclamados(self):
    try:
        with open(self._ruta_reclamados(), "w", encoding="utf-8") as f:
            json.dump(self.reclamados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        QMessageBox.warning(self, "Aviso", f"No se pudo guardar el histórico de reclamados:\n{e}")



def _clave_juego(self, juego):
    titulo = " ".join(str(juego.get("title") or "").lower().split()).strip()
    tienda = " ".join(str(self._asignar_tienda(juego) or "").lower().split()).strip()
    for sufijo in (" giveaway", " - giveaway"):
        if titulo.endswith(sufijo):
            titulo = titulo[:-len(sufijo)].strip()
    return f"game:{tienda}|{titulo}"



def _esta_reclamado(self, juego):
    clave_guardada = juego.get("__reclamado_key")
    if clave_guardada:
        return clave_guardada in self.reclamados
    return self._clave_juego(juego) in self.reclamados



def _abrir_reclamacion(self, url):
    if url:
        webbrowser.open(url)



def _alternar_reclamado(self, juego):
    clave = self._clave_juego(juego)
    estaba_reclamado = clave in self.reclamados
    if estaba_reclamado:
        del self.reclamados[clave]
    else:
        self.reclamados[clave] = {
            "key": clave,
            "id": juego.get("id"),
            "title": str(juego.get("title") or "Elemento sin título"),
            "store": self._asignar_tienda(juego),
            "image": juego.get("image") or juego.get("thumbnail"),
            "description": juego.get("description") or "",
            "open_giveaway_url": str(juego.get("open_giveaway_url") or ""),
            "worth": str(juego.get("worth") or ""),
            "worth_value": self._valor_juego(juego),
            "worth_currency": "USD",
            "claimed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    self._guardar_reclamados()
    self._actualizar_contador_ahorrado()
    if getattr(self, 'mostrando_reclamados', False):
        self._actualizar_vista_juegos()
        disponibles = [j for j in self.juegos_cache_global if not self._esta_reclamado(j)]
        conteos = {s: 0 for s in STORES_MAPPING.values()}
        for j in disponibles:
            tienda = self._asignar_tienda(j)
            if tienda in conteos: conteos[tienda] += 1
        self.actualizar_insignias(conteos)
        self._set_status(f"● {len(self.reclamados)} RECLAMADOS", "accent")
        return
    self._actualizar_vista_juegos()

    disponibles = [j for j in self.juegos_cache_global if not self._esta_reclamado(j)]
    conteos = {s: 0 for s in STORES_MAPPING.values()}
    for j in disponibles:
        tienda = self._asignar_tienda(j)
        if tienda in conteos:
            conteos[tienda] += 1
    self.actualizar_insignias(conteos)

    if self.mostrando_reclamados:
        self._set_status(f"● {len(self.reclamados)} RECLAMADOS", "accent")
    else:
        self._set_status(f"● {len(disponibles)} OFERTAS", "success")



def mostrar_reclamados(self):
    self.mostrando_reclamados = not self.mostrando_reclamados
    if self.mostrando_reclamados:
        self.btn_reclamados.setText("★ VER RECLAMADOS")
        self.btn_reclamados.setProperty("role", "accent")
        self._set_status("● LISTO", "success")
    else:
        self.btn_reclamados.setText("★ RECLAMADOS")
        self.btn_reclamados.setProperty("role", "secondary")
        disponibles = [j for j in self.juegos_cache_global if not self._esta_reclamado(j)]
        self._set_status(f"● {len(disponibles)} OFERTAS", "success")
    self.btn_reclamados.style().unpolish(self.btn_reclamados)
    self.btn_reclamados.style().polish(self.btn_reclamados)
    self._actualizar_visibilidad_atras()
    self._actualizar_vista_juegos()



def _mostrar_lista_reclamados(self):
    if not self.reclamados:
        label = QLabel("AÚN NO TIENES JUEGOS RECLAMADOS")
        label.setObjectName("emptyLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMinimumHeight(80)
        self.frame_lista_layout.addWidget(label)
        self.frame_lista_layout.addStretch(1)
        return

    header = QFrame()
    header.setObjectName("storeHeader")
    header_layout = QHBoxLayout(header)
    header_layout.setContentsMargins(0, 0, 0, 0)
    title = QLabel(f"★  MIS RECLAMADOS  ·  {len(self.reclamados)}")
    title.setObjectName("gameTitle")
    title.setContentsMargins(14, 10, 14, 10)
    header_layout.addWidget(title)
    self.frame_lista_layout.addWidget(header)

    for registro in sorted(
        self.reclamados.values(),
        key=lambda x: str(x.get("claimed_at", "")),
        reverse=True,
    ):
        juego = {
            "id": registro.get("id"),
            "title": registro.get("title", "Elemento sin título"),
            "store": registro.get("store", ""),
            "image": registro.get("image"),
            "thumbnail": registro.get("image"),
            "description": registro.get("description", ""),
            "open_giveaway_url": registro.get("open_giveaway_url", ""),
            "worth": registro.get("worth", ""),
            "worth_value": registro.get("worth_value", 0),
            "__reclamado_key": registro.get("key"),
        }
        self.frame_lista_layout.addWidget(GameCard(self, juego, registro.get("store", "Otras Plataformas")))
    self.frame_lista_layout.addStretch(1)



def instalar_metodos(cls):

    cls._ruta_reclamados = _ruta_reclamados

    cls._cargar_reclamados = _cargar_reclamados

    cls._parsear_valor_juego = _parsear_valor_juego

    cls._valor_juego = _valor_juego

    cls._dinero_ahorrado = _dinero_ahorrado

    cls._actualizar_contador_ahorrado = _actualizar_contador_ahorrado

    cls._guardar_reclamados = _guardar_reclamados

    cls._clave_juego = _clave_juego

    cls._esta_reclamado = _esta_reclamado

    cls._abrir_reclamacion = _abrir_reclamacion

    cls._alternar_reclamado = _alternar_reclamado

    cls.mostrar_reclamados = mostrar_reclamados

    cls._mostrar_lista_reclamados = _mostrar_lista_reclamados


