import sys
import io
import os
import tkinter as tk
import traceback

# ============================================================
# AUDIO DE ARRANQUE
# Se inicia antes de cargar la interfaz.
# ============================================================

pygame = None
_audio_iniciado = False

try:
    import pygame
    from config import AUDIO_PATH

    if os.path.exists(AUDIO_PATH):
        pygame.mixer.init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512
        )

        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

        _audio_iniciado = True
        print("🎵 [STARTUP] Audio iniciado inmediatamente")
    else:
        print(f"⚠️ [STARTUP] Audio no encontrado: {AUDIO_PATH}")

except Exception as e:
    print(f"⚠️ [STARTUP] Error iniciando audio: {e}")


from logger import log_app_iniciada, log_app_cerrada, log_info
from core.autostart import habilitar_autostart, mostrar_notificacion, autostart_activo


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

    # La interfaz se importa después de iniciar el audio.
    from ui.splash_screen import mostrar_splash_inicio
    from ui.main_window import VentanaPrincipal

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
    except Exception:
        pass

    try:
        root.iconbitmap(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'assets',
                'logo.ico'
            )
        )
    except Exception:
        pass

    root.geometry("1x1+0+0")

    # ---- FINALIZAR SPLASH ----
    splash_cerrado = False

    fade_job = None

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

        try:
            # Usamos el mismo intérprete Tk de la aplicación.
            # Así las PhotoImage no quedan asociadas a un root destruido.
            app = VentanaPrincipal(parent=root, mostrar=False)

            # La ventana ya está construida, pero permanece invisible.
            try:
                app.ventana.attributes("-alpha", 0.0)
            except Exception:
                pass

            # Mostrar la ventana solo después de dejarla completamente transparente.
            try:
                app.ventana.deiconify()
            except Exception:
                pass

            # Fade-in suave de la ventana principal.
            def fade_in_principal(alpha=0.0):
                try:
                    alpha += 0.05

                    if alpha >= 1.0:
                        app.ventana.attributes("-alpha", 1.0)
                        return

                    app.ventana.attributes("-alpha", alpha)
                    app.ventana.after(15, lambda: fade_in_principal(alpha))

                except Exception:
                    pass

            fade_in_principal()

            # Esperamos a que se cierre la ventana principal.
            app.run()

            # Al cerrar la app, detenemos completamente el audio.
            try:
                if _audio_iniciado and pygame is not None:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                        pygame.mixer.quit()
                        _audio_iniciado = False
            except Exception:
                pass

            # Ahora sí podemos destruir el root oculto.
            try:
                root.destroy()
            except Exception:
                pass

        except Exception as e:
            log_info(f"❌ Error creando la ventana principal: {e}")
            traceback.print_exc()

            try:
                if _audio_iniciado and pygame is not None:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                        pygame.mixer.quit()
            except Exception:
                pass

            try:
                root.destroy()
            except Exception:
                pass

            sys.exit(1)
    try:
        mostrar_splash_inicio(root, al_terminar_splash)
        root.mainloop()

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

    finally:
        # ---- SEGURIDAD: DETENER AUDIO SIEMPRE ----
        try:
            if _audio_iniciado and pygame is not None:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
        except Exception:
            pass

        log_app_cerrada()

        try:
            sys.exit(0)
        except SystemExit:
            pass
        except Exception:
            os._exit(0)


if __name__ == "__main__":
    main()





