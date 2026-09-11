import sys
import io
import os
import traceback

from logger import log_app_iniciada, log_app_cerrada, log_info

# Sanitizar salidas de texto estándar
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
# ============================================================

DURACION_ENTRADA_MS = 400
DURACION_ESPERA_MS = 1000
DURACION_SALIDA_MS = 400
SPLASH_LOGO_SIZE = 460


def _ruta_logo_splash():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "icons",
        "KGLogo.png",
    )


def _crear_splash(app):
    from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QLabel, QWidget

    ruta_logo = _ruta_logo_splash()
    logo = QPixmap(ruta_logo)

    if logo.isNull():
        log_info(f"⚠️ [SPLASH] Logo no encontrado: {ruta_logo}")
        return None, None

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

    app = QApplication.instance() or QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    splash = None
    try:
        splash, _ = _crear_splash(app)
        ventana = VentanaPrincipal(mostrar=False)

        def mostrar_principal():
            ventana.show()
            ventana.raise_()
            ventana.activateWindow()

        if splash is None:
            mostrar_principal()
        else:
            tiempo_total = DURACION_ENTRADA_MS + DURACION_ESPERA_MS + DURACION_SALIDA_MS
            QTimer.singleShot(tiempo_total, mostrar_principal)

        return app.exec()

    except KeyboardInterrupt:
        return 0
    except Exception as e:
        log_info(f"❌ Error fatal en aplicación: {e}")
        traceback.print_exc()
        return 1
    finally:
        try:
            log_app_cerrada()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
