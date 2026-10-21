from unittest.mock import patch

from core.tray import GameTrackerTray, enviar_notificacion_windows


class _VentanaBusqueda:
    _busqueda_en_curso = False

    def buscar_juegos(self):
        return True


def _tray_minima():
    tray = GameTrackerTray.__new__(GameTrackerTray)
    tray.ventana = _VentanaBusqueda()
    return tray


def test_barrido_notifies_only_after_search_completes():
    tray = _tray_minima()
    avisos = []
    tray._reportar_resultado_barrido = lambda manual=False: avisos.append(manual)

    tray._lanzar_busqueda(manual=False)
    assert avisos == []

    tray.completar_barrido()
    assert avisos == [False]
    tray.completar_barrido()
    assert avisos == [False]


def test_barrido_does_not_overlap_an_active_search():
    tray = _tray_minima()
    tray.ventana._busqueda_en_curso = True
    avisos = []
    tray._reportar_resultado_barrido = lambda manual=False: avisos.append(manual)

    tray._lanzar_busqueda(manual=True)
    assert avisos == []
    assert getattr(tray, "_barrido_notificacion_pendiente", None) is None


def test_notification_failure_is_logged_as_failure_not_success():
    class _Thread:
        def __init__(self, target, daemon):
            self.target = target

        def start(self):
            self.target()

    with (
        patch("core.tray.threading.Thread", _Thread),
        patch("plyer.notification.notify", side_effect=RuntimeError("Windows notification unavailable")),
        patch("core.tray.log_warning") as warning,
        patch("core.tray.log_info") as info,
    ):
        enviar_notificacion_windows("test", "body")

    warning.assert_called_once()
    assert "Windows notification unavailable" in warning.call_args.args[0]
    info.assert_not_called()
