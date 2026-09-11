"""Gestor de autostart y notificaciones del sistema."""

import os
import sys
import winreg
from logger import log_info, log_error


AUTOSTART_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
AUTOSTART_APP_NAME = "KGameTracker"


def habilitar_autostart():
    """Registra la app en autostart de Windows."""
    try:
        # Ruta completa del ejecutable
        ruta_app = os.path.abspath(sys.argv[0])
        if ruta_app.endswith('.py'):
            ruta_app = f'"{sys.executable}" "{ruta_app}"'
        else:
            ruta_app = f'"{ruta_app}"'
        
        # Abrir/crear clave de registro
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, AUTOSTART_APP_NAME, 0, winreg.REG_SZ, ruta_app)
        
        log_info("✅ Autostart habilitado")
        return True
        
    except Exception as e:
        log_error(f"Error habilitando autostart: {e}")
        return False


def deshabilitar_autostart():
    """Elimina la app del autostart."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, AUTOSTART_APP_NAME)
        
        log_info("❌ Autostart deshabilitado")
        return True
        
    except Exception as e:
        log_error(f"Error deshabilitando autostart: {e}")
        return False


def autostart_activo():
    """Verifica si el autostart está activo."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH) as key:
            winreg.QueryValueEx(key, AUTOSTART_APP_NAME)
            return True
    except FileNotFoundError:
        return False


def mostrar_notificacion(titulo, mensaje, duracion=5):
    """Muestra una notificación nativa del sistema usando plyer.

    Antes esto se hacía lanzando un script de PowerShell que construía un
    Toast XML a mano. Ese script tenía un bug real: el here-string de
    PowerShell (@"..."@) se cerraba con "@ indentado, y PowerShell exige
    que el cierre esté al principio de la línea, así que el script nunca
    llegaba a ejecutarse correctamente (el error quedaba oculto porque
    stdout/stderr se mandaban a DEVNULL). plyer ya estaba en
    requirements.txt sin usarse en ningún sitio: es la vía más simple y
    fiable de mostrar una notificación nativa en Windows.
    """
    try:
        from plyer import notification
        notification.notify(
            title=titulo,
            message=mensaje,
            app_name="K GAME TRACKER",
            timeout=duracion
        )
        log_info(f"📢 Notificación: {titulo}")
        return True

    except Exception as e:
        log_error(f"Error mostrando notificación: {e}")
        return False

