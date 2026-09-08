import sys
import io
import os
import tkinter as tk
import traceback

from logger import log_app_iniciada, log_app_cerrada, log_info
from core.autostart import habilitar_autostart, mostrar_notificacion, autostart_activo
from ui.splash_screen import mostrar_splash_inicio
from ui.main_window import VentanaPrincipal

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Punto de entrada de la aplicación."""
    log_app_iniciada()

    # ---- AUTOSTART ----
    try:
        if not autostart_activo():
            habilitar_autostart()
            mostrar_notificacion(
                "K GAME TRACKER",
                "App iniciada. Se ejecutará al encender el PC.",
                duracion=3
            )
    except Exception as e:
        log_info(f"⚠️ Autostart: {e}")

    # ---- CREAR ROOT ----
    root = tk.Tk()
    root.withdraw()
    try:
        root.configure(bg='#1e1e2e')
    except:
        pass
    try:
        root.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo.ico'))
    except Exception:
        pass
    root.geometry("1x1+0+0")

    # ---- INICIAR AUDIO DURANTE EL SPLASH ----
    fade_job = None
    try:
        import pygame
        from config import AUDIO_PATH
        if os.path.exists(AUDIO_PATH):
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.music.load(AUDIO_PATH)
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(-1)
            print('🎵 [SPLASH] Audio iniciado')
            
            def fade_in(vol=0):
                nonlocal fade_job
                if vol <= 20 and not splash_cerrado:
                    pygame.mixer.music.set_volume(vol / 100.0)
                    fade_job = root.after(100, lambda: fade_in(vol + 1))
            fade_job = root.after(100, lambda: fade_in(1))
        else:
            print(f'⚠️ [SPLASH] Audio no encontrado: {AUDIO_PATH}')
    except Exception as e:
        print(f'⚠️ [SPLASH] Error iniciando audio: {e}')

    splash_cerrado = False

    def al_terminar_splash():
        nonlocal splash_cerrado
        if splash_cerrado:
            return
        splash_cerrado = True
        if fade_job is not None:
            try:
                root.after_cancel(fade_job)
            except Exception:
                pass
        root.destroy()
        try:
            app = VentanaPrincipal()
        except Exception as e:
            log_info(f"❌ Error creando la ventana principal: {e}")
            traceback.print_exc()
            sys.exit(1)
            return
        app.run()
        sys.exit(0)

    try:
        mostrar_splash_inicio(root, al_terminar_splash)
        root.mainloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        log_app_cerrada()
        try:
            sys.exit(0)
        except SystemExit:
            pass
        except Exception:
            os._exit(0)

if __name__ == "__main__":
    main()
