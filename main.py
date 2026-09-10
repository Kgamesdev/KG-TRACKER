import sys
import io
import os
import traceback

# Igualar el escalado físico de Qt al de la aplicación Tk original.
# Evita que Windows (p. ej. 125%) agrande toda la interfaz Qt.
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

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


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ============================================================
# SPLASH Qt — KGLogo
# Splash independiente y nativo de Qt.
# Usa exclusivamente assets/icons/KGLogo.png, conservando su
# transparencia y su nitidez mediante SmoothTransformation.
# ============================================================

DURACION_ENTRADA_MS = 500
DURACION_ESPERA_MS = 1500
DURACION_SALIDA_MS = 500
SPLASH_LOGO_SIZE = 460


def _ruta_logo_splash():
    """Devuelve la ruta del nuevo logo dedicado al splash."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "icons",
        "KGLogo.png",
    )


def _crear_splash(app):
    """Crea el splash Qt con KGLogo y una entrada/salida por alfa."""
    from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QLabel, QWidget

    ruta_logo = _ruta_logo_splash()
    logo = QPixmap(ruta_logo)

    if logo.isNull():
        print(f"⚠️ [SPLASH] Logo no encontrado: {ruta_logo}")
        return None, None

    # El original es grande; se reduce solo para presentación.
    # Qt mantiene el canal alfa y usa interpolación suave para evitar
    # bordes dentados o pérdida visible de nitidez.
    logo = logo.scaled(
        SPLASH_LOGO_SIZE,
        SPLASH_LOGO_SIZE,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )

    splash = QWidget(
        None,
        Qt.WindowType.FramelessWindowHint
        | Qt.WindowType.Tool
        | Qt.WindowType.WindowStaysOnTopHint
        | Qt.WindowType.WindowDoesNotAcceptFocus
        | Qt.WindowType.WindowTransparentForInput,
    )
    splash.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    splash.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
    splash.setFixedSize(logo.size())

    label = QLabel(splash)
    label.setPixmap(logo)
    label.setFixedSize(logo.size())
    label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    label.setStyleSheet("background: transparent; border: none;")
    label.move(0, 0)

    screen = app.primaryScreen()
    if screen is not None:
        geometry = screen.availableGeometry()
        x = geometry.x() + (geometry.width() - splash.width()) // 2
        y = geometry.y() + (geometry.height() - splash.height()) // 2
        splash.move(x, y)

    splash.setWindowOpacity(0.0)
    splash.show()
    app.processEvents()

    entrada = QPropertyAnimation(splash, b"windowOpacity", splash)
    entrada.setDuration(DURACION_ENTRADA_MS)
    entrada.setStartValue(0.0)
    entrada.setEndValue(1.0)
    entrada.setEasingCurve(QEasingCurve.Type.InOutCubic)

    salida = QPropertyAnimation(splash, b"windowOpacity", splash)
    salida.setDuration(DURACION_SALIDA_MS)
    salida.setStartValue(1.0)
    salida.setEndValue(0.0)
    salida.setEasingCurve(QEasingCurve.Type.InOutCubic)

    estado = {
        "entrada": entrada,
        "salida": salida,
        "finalizado": False,
    }

    def finalizar():
        if estado["finalizado"]:
            return

        estado["finalizado"] = True
        splash.close()
        splash.deleteLater()

    def iniciar_salida():
        if estado["finalizado"]:
            return
        salida.finished.connect(finalizar)
        salida.start()

    entrada.finished.connect(
        lambda: QTimer.singleShot(DURACION_ESPERA_MS, iniciar_salida)
    )

    entrada.start()

    return splash, estado


def main():
    """Punto de entrada de la aplicación."""

    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication
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

    app = QApplication.instance() or QApplication(sys.argv)

    splash = None

    try:
        splash, _splash_estado = _crear_splash(app)

        # La ventana principal se crea oculta durante el splash.
        ventana = VentanaPrincipal(mostrar=False)

        def mostrar_principal():
            ventana.show()
            ventana.raise_()
            ventana.activateWindow()

        if splash is None:
            mostrar_principal()
        else:
            QTimer.singleShot(
                DURACION_ENTRADA_MS
                + DURACION_ESPERA_MS
                + DURACION_SALIDA_MS,
                mostrar_principal
            )

        codigo = app.exec()

        # Al cerrar la app, detenemos completamente el audio.
        try:
            if _audio_iniciado and pygame is not None:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    globals()["_audio_iniciado"] = False
        except Exception:
            pass

        return codigo

    except KeyboardInterrupt:
        return 0

    except Exception as e:
        log_info(f"❌ Error creando la aplicación: {e}")
        traceback.print_exc()

        try:
            if _audio_iniciado and pygame is not None:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    globals()["_audio_iniciado"] = False
        except Exception:
            pass

        return 1

    finally:
        try:
            log_app_cerrada()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
