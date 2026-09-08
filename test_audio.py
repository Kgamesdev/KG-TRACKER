# ============================================================
# SCRIPT DE PRUEBA DE AUDIO (PYGAME)
# ============================================================
import os
import pygame

# Configurar ruta
AUDIO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chill.wav")

print(f"🔍 Buscando audio en: {AUDIO_PATH}")

if not os.path.exists(AUDIO_PATH):
    print("❌ NO existe el archivo chill.wav")
    exit(1)

print("✅ Archivo encontrado")

try:
    print("🎵 Inicializando pygame.mixer...")
    pygame.mixer.init()
    
    print("🎵 Cargando audio...")
    pygame.mixer.music.load(AUDIO_PATH)
    
    print("🎵 Reproduciendo... (volumen 10%)")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    
    print("🎵 Audio reproduciéndose. Esperando 3 segundos...")
    import time
    time.sleep(3)
    
    print("🎵 Deteniendo audio...")
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    
    print("✅ PRUEBA EXITOSA")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()