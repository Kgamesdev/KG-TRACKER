import sys

import io

import os

import traceback



from logger import log_app_iniciada, log_app_cerrada, log_info, log_error, log_warning



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

    app = QApplication.instance() or QApplication(sys.argv)

    from core.single_instance import SingleInstance

    app.setApplicationName("KGameTracker")
    gestor_instancia = SingleInstance()

    if not gestor_instancia.is_primary:
        if getattr(gestor_instancia, "activation_sent", False):
            log_info("[APP] Ya hay una instancia abierta; se solicitó mostrar su ventana.")
        else:
            log_warning("[APP] Inicio bloqueado: no se pudo adquirir la instancia única ni contactar con la instancia activa.")
        gestor_instancia.close()
        return 0

    from ui.main_window import VentanaPrincipal
    from core.tray import GameTrackerTray

    log_app_iniciada()

    app.setQuitOnLastWindowClosed(False)



    splash = None

    try:

        splash, _ = _crear_splash(app)

        ventana = VentanaPrincipal(mostrar=False)

        ventana._tray = GameTrackerTray(ventana)

        def _al_cerrar_app():
            try:
                from core.translator import GameTranslator
                if GameTranslator._instancia:
                    GameTranslator._instancia.detener()
            except Exception:
                pass

            try:
                if hasattr(ventana, "_esperar_hilo_busqueda"):
                    ventana._esperar_hilo_busqueda(timeout_ms=15000)
                elif hasattr(ventana, "_limpiar_hilo_busqueda"):
                    ventana._limpiar_hilo_busqueda()
            except Exception as error_busqueda:
                log_error(f"Error cerrando el hilo de búsqueda: {error_busqueda}", exc_info=True)

            try:
                if hasattr(ventana, "_detener_audio"):
                    ventana._detener_audio()
            except Exception:
                pass

            try:
                from PySide6.QtCore import QThreadPool
                pool = QThreadPool.globalInstance()
                pool.clear()
                terminado = pool.waitForDone(15000)
                if not terminado:
                    log_warning("Siguen finalizando tareas de fondo durante el cierre.")
                    pool.waitForDone()
            except Exception:
                pass

        app.aboutToQuit.connect(_al_cerrar_app)



        def mostrar_principal():
            # El splash se autodestruye al terminar su animación. Si la
            # activación de otra instancia llega después, el wrapper Python
            # puede seguir existiendo aunque su QWidget C++ ya no exista.
            if splash is not None:
                try:
                    from shiboken6 import isValid
                    if isValid(splash) and splash.isVisible():
                        splash.close()
                except RuntimeError:
                    pass

            ventana._tray.mostrar_ventana()


        gestor_instancia.activation_requested.connect(mostrar_principal)



        if splash is None:

            mostrar_principal()

        else:

            tiempo_total = DURACION_ENTRADA_MS + DURACION_ESPERA_MS + DURACION_SALIDA_MS

            QTimer.singleShot(tiempo_total, mostrar_principal)



        return app.exec()



    except KeyboardInterrupt:

        return 0

    except Exception as e:

        log_error(f"Error fatal en aplicación: {e}", exc_info=True)

        traceback.print_exc()

        return 1

    finally:

        try:

            gestor_instancia.close()

        except Exception:

            pass

        try:

            log_app_cerrada()

        except Exception:

            pass





if __name__ == "__main__":

    sys.exit(main())

