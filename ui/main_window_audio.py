"""Gestión de audio de la ventana principal."""

import os
import json
try:
    import pygame
except Exception as error:
    pygame = None
    from logger import log_warning
    log_warning(f"Audio desactivado: no se pudo cargar pygame ({error}).")
from PySide6.QtCore import QTimer
from config import AUDIO_PATH
from logger import log_error
from core.paths import SETTINGS_FILE


def _config_audio():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos if isinstance(datos, dict) else {}
    except Exception:
        return {}


def _guardar_estado_audio(self):
    """Guarda las preferencias actuales de música y volumen."""
    try:
        datos = _config_audio()
        datos["musica_activa"] = bool(getattr(self, "_musica_preferida", True))
        datos["musica_silenciada"] = bool(getattr(self, "audio_silenciado", False))
        if getattr(self, "slider_volumen", None) is not None:
            volumen = int(self.slider_volumen.value())
            if volumen > 0:
                self.volumen_anterior = volumen
            datos["volumen_musica"] = int(getattr(self, "volumen_anterior", 5))
        from core.storage import guardar_json_atomico
        if not guardar_json_atomico(SETTINGS_FILE, datos):
            log_error("No se pudo guardar el estado de la música; los cambios podrían perderse al cerrar.")
    except Exception as error:
        log_error(f"No se pudo guardar el estado de la música: {error}")


def _actualizar_icono_mute(self):
    if self.btn_mute is not None:
        icono = "mute.png" if self.audio_silenciado or not self._musica_preferida else "volume.png"
        self.btn_mute.set_icon(self._icon_path(icono))


def _inicializar_audio(self):
    """Prepara el mezclador y respeta la preferencia persistente de música."""
    ajustes = _config_audio()
    self._musica_preferida = bool(ajustes.get("musica_activa", True))
    self.volumen_anterior = max(1, min(100, int(ajustes.get("volumen_musica", 5) or 5)))
    self.audio_silenciado = bool(ajustes.get("musica_silenciada", False)) or not self._musica_preferida

    # Estos controles siguen disponibles aunque la música esté desactivada.
    self.slider_volumen.setEnabled(True)
    self.btn_mute.setEnabled(True)
    if not self._musica_preferida or self.audio_silenciado:
        self.slider_volumen.blockSignals(True)
        self.slider_volumen.setValue(0 if self.audio_silenciado else self.volumen_anterior)
        self.slider_volumen.blockSignals(False)
        if pygame is not None and pygame.mixer.get_init():
            pygame.mixer.music.stop()
        _actualizar_icono_mute(self)
        return

    self.slider_volumen.setEnabled(True)
    self.btn_mute.setEnabled(True)
    try:
        if pygame is None or not os.path.exists(AUDIO_PATH):
            self.audio_silenciado = True
            _actualizar_icono_mute(self)
            return

        if not pygame.mixer.get_init():
            pygame.mixer.init(
                frequency=44100,
                size=-16,
                channels=2,
                buffer=512,
            )

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.abspath(AUDIO_PATH))
            pygame.mixer.music.set_volume(self.volumen_anterior / 100.0)
            pygame.mixer.music.play(-1)

        self.audio_silenciado = False
        volumen_actual = int(round(pygame.mixer.music.get_volume() * 100))
        if volumen_actual <= 0:
            volumen_actual = self.volumen_anterior
            pygame.mixer.music.set_volume(volumen_actual / 100.0)
        self.slider_volumen.blockSignals(True)
        self.slider_volumen.setValue(volumen_actual)
        self.slider_volumen.blockSignals(False)
        _actualizar_icono_mute(self)

    except Exception as e:
        self.audio_silenciado = True
        _actualizar_icono_mute(self)
        log_error(f"No se pudo inicializar el audio: {e}")



def _fade_audio(self, porcentaje):
    try:
        if pygame is None or not pygame.mixer.get_init():
            return
        porcentaje = max(0, min(20, porcentaje))
        pygame.mixer.music.set_volume(porcentaje / 100.0)
        self.slider_volumen.blockSignals(True)
        self.slider_volumen.setValue(porcentaje)
        self.slider_volumen.blockSignals(False)
        if porcentaje < 20:
            QTimer.singleShot(100, lambda: self._fade_audio(porcentaje + 1))
    except Exception:
        pass



def cambiar_volumen(self, valor):
    try:
        if self.btn_mute is None:
            return
        porcentaje = max(0, min(100, int(float(valor))))
        if porcentaje > 0:
            self.volumen_anterior = porcentaje
            self.audio_silenciado = False
            self._musica_preferida = True
            if pygame is not None:
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                pygame.mixer.music.set_volume(porcentaje / 100.0)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(os.path.abspath(AUDIO_PATH))
                    pygame.mixer.music.play(-1)
        else:
            self.audio_silenciado = True
            if pygame is not None and pygame.mixer.get_init():
                pygame.mixer.music.set_volume(0.0)
        _actualizar_icono_mute(self)
        _guardar_estado_audio(self)
    except Exception as e:
        log_error(f"Error cambiando volumen: {e}")



def alternar_mute(self):
    try:
        if pygame is None:
            return
        if not self.audio_silenciado:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            valor_actual = int(self.slider_volumen.value())
            if valor_actual > 0:
                self.volumen_anterior = valor_actual
            pygame.mixer.music.set_volume(0.0)
            self.slider_volumen.blockSignals(True)
            self.slider_volumen.setValue(0)
            self.slider_volumen.blockSignals(False)
            self.audio_silenciado = True
        else:
            vol = self.volumen_anterior if self.volumen_anterior > 0 else 10
            self._musica_preferida = True
            self.audio_silenciado = False
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.music.set_volume(vol / 100.0)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.abspath(AUDIO_PATH))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(vol / 100.0)
            self.slider_volumen.blockSignals(True)
            self.slider_volumen.setValue(vol)
            self.slider_volumen.blockSignals(False)
        _actualizar_icono_mute(self)
        _guardar_estado_audio(self)
    except Exception as e:
        log_error(f"Error alternando mute: {e}")


def aplicar_preferencia_musica(self, activa):
    self._musica_preferida = bool(activa)
    if not activa:
        self.audio_silenciado = True
        if pygame is not None and pygame.mixer.get_init():
            pygame.mixer.music.stop()
        self.slider_volumen.blockSignals(True)
        self.slider_volumen.setValue(self.volumen_anterior)
        self.slider_volumen.blockSignals(False)
        self.slider_volumen.setEnabled(True)
        self.btn_mute.setEnabled(True)
        _actualizar_icono_mute(self)
        _guardar_estado_audio(self)
        return

    self.slider_volumen.setEnabled(True)
    self.btn_mute.setEnabled(True)
    self.audio_silenciado = False
    _guardar_estado_audio(self)
    _inicializar_audio(self)
    _guardar_estado_audio(self)



def _detener_audio(self):
    try:
        if pygame is not None and pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass



def instalar_metodos(cls):

    cls._inicializar_audio = _inicializar_audio

    cls._fade_audio = _fade_audio

    cls.cambiar_volumen = cambiar_volumen

    cls.alternar_mute = alternar_mute

    cls.aplicar_preferencia_musica = aplicar_preferencia_musica

    cls._detener_audio = _detener_audio


