"""Modulo de integracion con la bandeja del sistema (System Tray) y eventos de cierre."""
from PySide6.QtCore import QTimer
from core.tray import GameTrackerTray


def _iniciar_fade_audio(self, objetivo, duracion_ms=700, callback_final=None):
    """Reduce o sube el volumen de audio suavemente."""
    try:
        import pygame
        mixer_activo = pygame.mixer.get_init()
    except Exception:
        mixer_activo = False

    pasos = 18
    intervalo = max(10, duracion_ms // pasos)

    if mixer_activo:
        import pygame
        vol_actual = pygame.mixer.music.get_volume()
    elif hasattr(self, "audio_output") and self.audio_output:
        vol_actual = self.audio_output.volume()
    else:
        if callback_final:
            callback_final()
        return

    diff = objetivo - vol_actual
    if abs(diff) < 0.01:
        if callback_final:
            callback_final()
        return

    paso_vol = diff / pasos
    estado = {"paso": 0}

    def tick():
        estado["paso"] += 1
        nuevo = max(0.0, min(1.0, vol_actual + (paso_vol * estado["paso"])))
        if mixer_activo:
            import pygame
            pygame.mixer.music.set_volume(nuevo)
        elif hasattr(self, "audio_output") and self.audio_output:
            self.audio_output.setVolume(nuevo)

        if estado["paso"] >= pasos:
            timer.stop()
            timer.deleteLater()
            if mixer_activo:
                import pygame
                pygame.mixer.music.set_volume(objetivo)
            elif hasattr(self, "audio_output") and self.audio_output:
                self.audio_output.setVolume(objetivo)
            if callback_final:
                callback_final()

    timer = QTimer(self)
    timer.setInterval(intervalo)
    timer.timeout.connect(tick)
    timer.start()


def pausar_musica_con_fade(self):
    def al_pausar():
        try:
            import pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.pause()
        except Exception:
            pass
    self._iniciar_fade_audio(0.0, duracion_ms=600, callback_final=al_pausar)


def reanudar_musica_con_fade(self):
    from config import AUDIO_VOLUME_TARGET
    vol_destino = getattr(self, "volumen_actual", AUDIO_VOLUME_TARGET)
    try:
        import pygame
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()
    except Exception:
        pass
    self._iniciar_fade_audio(vol_destino, duracion_ms=800)


def closeEvent(self, event):
    if getattr(self, "_salida_forzada", False):
        if hasattr(self, "_tray") and self._tray and self._tray.tray_icon:
            self._tray.tray_icon.hide()
        event.accept()
        return

    event.ignore()
    self.pausar_musica_con_fade()
    self.hide()
    if hasattr(self, "_tray") and self._tray:
        self._tray.notificar_primer_cierre()


def inicializar_tray(self):
    self._salida_forzada = False
    try:
        self._tray = GameTrackerTray(self)
    except Exception:
        self._tray = None


def instalar_metodos(cls):
    cls._iniciar_fade_audio = _iniciar_fade_audio
    cls.pausar_musica_con_fade = pausar_musica_con_fade
    cls.reanudar_musica_con_fade = reanudar_musica_con_fade
    cls.closeEvent = closeEvent
    cls.inicializar_tray = inicializar_tray
