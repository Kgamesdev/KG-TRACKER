"""Modulo de integracion con la bandeja del sistema (System Tray) y eventos de cierre."""
import json
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from core.tray import GameTrackerTray
from core.paths import SETTINGS_FILE


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
    if not getattr(self, "_musica_preferida", True) or getattr(self, "audio_silenciado", False):
        return

    def al_pausar():
        try:
            import pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.pause()
        except Exception:
            pass
    self._iniciar_fade_audio(0.0, duracion_ms=600, callback_final=al_pausar)


def reanudar_musica_con_fade(self):
    if not getattr(self, "_musica_preferida", True) or getattr(self, "audio_silenciado", False):
        return
    vol_destino = max(0.0, min(1.0, self.slider_volumen.value() / 100.0))
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

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as archivo:
            minimizar = bool(json.load(archivo).get("minimizar_al_cerrar", False))
    except Exception:
        minimizar = False
    if minimizar:
        event.ignore()
        self._minimizar_a_bandeja()
        return

    # El botón X sale completamente. El menú de bandeja sigue ofreciendo
    # una salida explícita y comparte este mismo camino.
    self._salida_forzada = True
    if hasattr(self, "_tray") and self._tray and self._tray.tray_icon:
        self._tray.tray_icon.hide()
    if hasattr(self, "_guardar_estado_audio"):
        self._guardar_estado_audio()
    self._detener_audio()
    event.accept()
    app = QApplication.instance()
    if app:
        app.quit()


def _minimizar_a_bandeja(self):
    self.pausar_musica_con_fade()
    self.hide()
    if hasattr(self, "_tray") and self._tray:
        self._tray.notificar_al_minimizar()


def changeEvent(self, event):
    from PySide6.QtCore import QEvent
    super(type(self), self).changeEvent(event)
    if event.type() == QEvent.Type.WindowStateChange and self.isMinimized():
        QTimer.singleShot(0, self._minimizar_a_bandeja)


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
    cls.changeEvent = changeEvent
    cls._minimizar_a_bandeja = _minimizar_a_bandeja
    cls.inicializar_tray = inicializar_tray
