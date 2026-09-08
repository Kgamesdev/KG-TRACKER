"""Gestor de audio con fade-in real en WAV (sin dependencias externas)."""

import os
import threading
import wave
import struct
import subprocess
from logger import log_info, log_error


class GestorAudio:
    """Gestor de audio con fade-in real aplicado al WAV."""
    
    def __init__(self, ruta_audio=None, volumen_objetivo=0.1, duracion_fade=3.0):
        """Inicializa el gestor de audio."""
        self.ruta_audio = ruta_audio
        self.volumen_objetivo = volumen_objetivo
        self.duracion_fade = duracion_fade
        self.hilo_audio = None
        self.reproduciendo = False
        self.proceso_audio = None
        
        log_info("✅ Sistema de audio (WAV fade-in) inicializado")
    
    def _aplicar_fade_in_wav(self, ruta_entrada, ruta_salida):
        """
        Aplica fade-in + reduce volumen a objetivo.
        El audio completo se queda al volumen_objetivo (10%).
        Los primeros 3 segundos hacen fade-in de 0% a 100% del volumen objetivo.
        """
        try:
            with wave.open(ruta_entrada, 'rb') as wav_entrada:
                # Leer parámetros del WAV
                n_canales = wav_entrada.getnchannels()
                sample_width = wav_entrada.getsampwidth()
                framerate = wav_entrada.getframerate()
                n_frames = wav_entrada.getnframes()
                
                # Leer todos los samples
                frames = wav_entrada.readframes(n_frames)
            
            # Calcular cuántos samples necesita el fade-in
            muestras_fade = int(framerate * self.duracion_fade)
            muestras_fade = min(muestras_fade, n_frames)
            
            # Convertir bytes a lista de integers
            if sample_width == 1:
                samples = list(struct.unpack(f'<{n_frames * n_canales}B', frames))
            elif sample_width == 2:
                samples = list(struct.unpack(f'<{n_frames * n_canales}h', frames))
            elif sample_width == 4:
                samples = list(struct.unpack(f'<{n_frames * n_canales}i', frames))
            else:
                log_error(f"Formato WAV no soportado: {sample_width} bytes")
                return False
            
            # 1. Reducir volumen COMPLETO a 10%
            for i in range(len(samples)):
                samples[i] = int(samples[i] * self.volumen_objetivo)
            
            # 2. Aplicar fade-in (0% a 100% del volumen de 10%)
            for i in range(muestras_fade * n_canales):
                posicion_en_fade = i / (muestras_fade * n_canales)
                factor = posicion_en_fade
                samples[i] = int(samples[i] * factor)
            
            # Convertir lista de integers de vuelta a bytes
            if sample_width == 1:
                frames = struct.pack(f'<{len(samples)}B', *samples)
            elif sample_width == 2:
                frames = struct.pack(f'<{len(samples)}h', *samples)
            elif sample_width == 4:
                frames = struct.pack(f'<{len(samples)}i', *samples)
            
            # Escribir WAV con fade-in
            with wave.open(ruta_salida, 'wb') as wav_salida:
                wav_salida.setnchannels(n_canales)
                wav_salida.setsampwidth(sample_width)
                wav_salida.setframerate(framerate)
                wav_salida.writeframes(frames)
            
            log_info(f"🎚️  Volumen: {self.volumen_objetivo*100:.0f}% | Fade-in: {self.duracion_fade}s")
            return True
            
        except Exception as e:
            log_error(f"Error aplicando fade-in: {e}")
            return False
    
    def reproducir_con_fade_in(self):
        """Inicia la reproducción con fade-in."""
        # Resolver ruta absoluta
        if not os.path.isabs(self.ruta_audio):
            ruta_absoluta = os.path.join(os.getcwd(), self.ruta_audio)
        else:
            ruta_absoluta = self.ruta_audio
        
        if not os.path.exists(ruta_absoluta):
            log_error(f"Archivo no encontrado: {ruta_absoluta}")
            return
        
        # Crear hilo para reproducción
        self.hilo_audio = threading.Thread(
            target=self._ejecutar_fade_in,
            args=(ruta_absoluta,),
            daemon=True
        )
        self.hilo_audio.start()
    
    def _ejecutar_fade_in(self, ruta_absoluta):
        """Ejecuta el fade-in."""
        try:
            self.reproduciendo = True
            log_info(f"🎵 Procesando: {os.path.basename(ruta_absoluta)}")
            
            # Crear archivo WAV temporal con fade-in
            ruta_temp = os.path.join(os.path.dirname(ruta_absoluta), ".tmp_fade.wav")
            if not self._aplicar_fade_in_wav(ruta_absoluta, ruta_temp):
                log_error("No se pudo aplicar fade-in")
                return
            
            log_info(f"🔊 Reproduciendo con fade-in ({self.volumen_objetivo*100:.0f}%)...")
            
            # Reproducir con PowerShell/Media.SoundPlayer (controlable)
            cmd = f'(New-Object Media.SoundPlayer "{ruta_temp}").PlaySync()'
            self.proceso_audio = subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", cmd],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Esperar a que termine
            self.proceso_audio.wait()
            
            # Limpiar archivo temporal
            try:
                os.remove(ruta_temp)
            except:
                pass
            
            log_info(f"✅ Audio completado")
            self.reproduciendo = False
            self.proceso_audio = None
            
        except Exception as e:
            log_error(f"Error en audio: {e}")
            self.reproduciendo = False
            self.proceso_audio = None
    
    def detener_con_fade_out(self):
        """Detiene el audio."""
        if not self.reproduciendo:
            return
        
        # Matar el proceso de audio
        if self.proceso_audio:
            try:
                self.proceso_audio.terminate()
                self.proceso_audio.wait(timeout=1)
            except:
                try:
                    self.proceso_audio.kill()
                except:
                    pass
        
        self.reproduciendo = False
        self.proceso_audio = None
        log_info("🔇 Audio detenido")
    
    def detener_inmediatamente(self):
        """Detiene inmediatamente."""
        self.detener_con_fade_out()


# Instancia global
_gestor_audio = None


def inicializar_audio(ruta_audio, volumen_objetivo=0.1, duracion_fade=3.0):
    """Inicializa el audio."""
    global _gestor_audio
    _gestor_audio = GestorAudio(ruta_audio, volumen_objetivo, duracion_fade)
    return _gestor_audio


def reproducir_audio_inicio():
    """Inicia reproducción."""
    if _gestor_audio:
        _gestor_audio.reproducir_con_fade_in()


def detener_audio():
    """Detiene reproducción."""
    if _gestor_audio:
        _gestor_audio.detener_con_fade_out()


def obtener_gestor_audio():
    """Retorna el gestor."""
    return _gestor_audio

