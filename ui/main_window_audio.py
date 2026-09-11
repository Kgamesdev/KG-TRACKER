"""GestiÃƒÂ³n de audio de la ventana principal."""

import os
import pygame
from PySide6.QtCore import QTimer
from config import AUDIO_PATH


def _inicializar_audio(self):
    """Conserva la mÃƒÂºsica iniciada por main.py y evita reinicios/cortes."""
    try:
        if not os.path.exists(AUDIO_PATH):
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
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1)

        self.audio_silenciado = False
        self.volumen_anterior = 20
        volumen_actual = int(round(pygame.mixer.music.get_volume() * 100))
        if volumen_actual <= 0:
            volumen_actual = 5
            pygame.mixer.music.set_volume(volumen_actual / 100.0)
        self.slider_volumen.blockSignals(True)
        self.slider_volumen.setValue(volumen_actual)
        self.slider_volumen.blockSignals(False)

    except Exception as e:
        print(f"Ã¢Å¡Â Ã¯Â¸Â No se pudo inicializar el audio: {e}")



def _fade_audio(self, porcentaje):
    try:
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
        pygame.mixer.music.set_volume(porcentaje / 100.0)
        if porcentaje > 0:
            self.audio_silenciado = False
            self.volumen_anterior = porcentaje
            self.btn_mute.set_icon(self._icon_path("volume.png"))
        else:
            self.audio_silenciado = True
            self.btn_mute.set_icon(self._icon_path("mute.png"))
    except Exception as e:
        print(f"Ã¢Å¡Â Ã¯Â¸Â Error cambiando volumen: {e}")



def alternar_mute(self):
    try:
        if not self.audio_silenciado:
            self.volumen_anterior = int(self.slider_volumen.value())
            pygame.mixer.music.set_volume(0.0)
            self.slider_volumen.setValue(0)
            self.audio_silenciado = True
            self.btn_mute.set_icon(self._icon_path("mute.png"))
        else:
            vol = self.volumen_anterior if self.volumen_anterior > 0 else 10
            pygame.mixer.music.set_volume(vol / 100.0)
            self.slider_volumen.setValue(vol)
            self.audio_silenciado = False
            self.btn_mute.set_icon(self._icon_path("volume.png"))
    except Exception as e:
        print(f"Ã¢Å¡Â Ã¯Â¸Â Error alternando mute: {e}")



def _detener_audio(self):
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    except Exception:
        pass



def instalar_metodos(cls):

    cls._inicializar_audio = _inicializar_audio

    cls._fade_audio = _fade_audio

    cls.cambiar_volumen = cambiar_volumen

    cls.alternar_mute = alternar_mute

    cls._detener_audio = _detener_audio
