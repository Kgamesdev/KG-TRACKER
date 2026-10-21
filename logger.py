"""Sistema de logging centralizado para K Game Tracker.

Proporciona una manera consistente de registrar eventos, errores y debugging
en toda la aplicación.

Ejemplo de uso:
    from logger import log_info, log_error, log_warning
    
    log_info("App iniciada")
    log_error("Error al descargar imagen", exc_info=True)
    log_warning("Conexión lenta detectada")
"""

import logging
import os
import sys
import tempfile
from datetime import datetime

# Los logs viven en una ubicación escribible para el usuario. La carpeta de
# instalación puede estar bajo Program Files y ser de solo lectura.
try:
    from core.paths import LOGS_DIR as USER_LOGS_DIR
    LOGS_DIR = str(USER_LOGS_DIR)
except Exception:
    LOGS_DIR = os.path.join(os.path.expanduser("~"), ".kgtracker", "logs")

try:
    os.makedirs(LOGS_DIR, exist_ok=True)
except OSError:
    LOGS_DIR = os.path.join(tempfile.gettempdir(), "KGTracker", "logs")
    os.makedirs(LOGS_DIR, exist_ok=True)

# Nombre del archivo de log con fecha
LOG_FILE = os.path.join(LOGS_DIR, f"kgametracker_{datetime.now().strftime('%Y-%m-%d')}.log")

# Handlers: el archivo si está disponible y consola solo si existe.
_handlers = []
try:
    _handlers.append(logging.FileHandler(LOG_FILE, encoding="utf-8"))
except OSError:
    pass
if sys.stderr is not None:
    _handlers.append(logging.StreamHandler())
if not _handlers:
    _handlers.append(logging.NullHandler())

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=_handlers
)

# Obtener logger específico
logger = logging.getLogger("KGameTracker")


def _registrar_excepcion_no_controlada(tipo, valor, traza):
    """Deja un rastro de errores Python que, de otro modo, cerrarían la app."""
    if issubclass(tipo, KeyboardInterrupt):
        sys.__excepthook__(tipo, valor, traza)
        return
    logger.critical(
        "Excepción Python no controlada; la aplicación puede cerrarse.",
        exc_info=(tipo, valor, traza),
    )
    if sys.stderr is not None:
        sys.__excepthook__(tipo, valor, traza)


sys.excepthook = _registrar_excepcion_no_controlada


# =====================================================
# FUNCIONES DE CONVENIENCIA
# =====================================================

def log_info(mensaje):
    """
    Registra un mensaje informativo.
    
    Args:
        mensaje (str): Mensaje a registrar
        
    Ejemplo:
        log_info("Búsqueda iniciada")
    """
    logger.info(f"ℹ️  {mensaje}")


def log_warning(mensaje):
    """
    Registra una advertencia.
    
    Args:
        mensaje (str): Mensaje de advertencia
        
    Ejemplo:
        log_warning("Conexión lenta detectada")
    """
    logger.warning(f"⚠️  {mensaje}")


def log_error(mensaje, exc_info=False):
    """
    Registra un error.
    
    Args:
        mensaje (str): Mensaje de error
        exc_info (bool): Si True, incluye la traza completa de excepción
        
    Ejemplo:
        try:
            algo_que_falla()
        except Exception:
            log_error("Error en búsqueda", exc_info=True)
    """
    logger.error(f"❌ {mensaje}", exc_info=exc_info)


def log_success(mensaje):
    """
    Registra un evento exitoso.
    
    Args:
        mensaje (str): Mensaje de éxito
        
    Ejemplo:
        log_success("Juegos cargados correctamente")
    """
    logger.info(f"✅ {mensaje}")


def log_debug(mensaje):
    """
    Registra un mensaje de debug (solo en modo debug).
    
    Args:
        mensaje (str): Mensaje de debug
        
    Ejemplo:
        log_debug(f"Juego encontrado: {juego['title']}")
    """
    logger.debug(f"🔍 {mensaje}")


def obtener_ruta_log():
    """
    Retorna la ruta del archivo de log actual.
    
    Returns:
        str: Ruta completa del archivo de log
        
    Ejemplo:
        ruta = obtener_ruta_log()
        print(f"Logs guardados en: {ruta}")
    """
    return LOG_FILE


# =====================================================
# CONTEXTO MANAGER PARA CAPTURAR ERRORES
# =====================================================

class LogContext:
    """
    Context manager para registrar bloques de código con manejo automático de errores.
    
    Ejemplo:
        with LogContext("Descarga de imagen"):
            descargar_imagen(url)
    """
    
    def __init__(self, operacion):
        """
        Args:
            operacion (str): Nombre de la operación
        """
        self.operacion = operacion
    
    def __enter__(self):
        log_info(f"Iniciando: {self.operacion}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            log_success(f"Completado: {self.operacion}")
        else:
            log_error(
                f"Error en {self.operacion}: {exc_val}",
                exc_info=True
            )
        return False  # No suprimir la excepción


# =====================================================
# LOG DE EVENTOS ESPECIALES
# =====================================================

def log_búsqueda_iniciada(modo):
    """Registra cuando se inicia una búsqueda."""
    modo_texto = "Todo Gratis" if modo else "Solo Juegos"
    log_info(f"Búsqueda iniciada - Modo: {modo_texto}")


def log_juegos_encontrados(cantidad, tiendas):
    """Registra resultados de búsqueda."""
    log_success(
        f"Se encontraron {cantidad} juegos en {len(tiendas)} tiendas"
    )


def log_tienda_seleccionada(tienda, activo):
    """Registra cuando se selecciona/deselecciona una tienda."""
    estado = "✓ Seleccionada" if activo else "✗ Deseleccionada"
    log_debug(f"Tienda {estado}: {tienda}")


def log_error_conexión(url, error):
    """Registra errores de conexión."""
    log_error(f"Error de conexión a {url}: {error}")


def log_error_imagen(url, error):
    """Registra errores al descargar imágenes."""
    log_warning(f"No se pudo descargar imagen de {url}: {error}")


def log_app_iniciada():
    """Registra el inicio de la app."""
    log_info("=" * 50)
    log_info("K GAME TRACKER - INICIADA")
    log_info("=" * 50)


def log_app_cerrada():
    """Registra el cierre de la app."""
    log_info("=" * 50)
    log_info("K GAME TRACKER - CERRADA")
    log_info("=" * 50)
