"""Sistema de logging centralizado para K Game Tracker.

Proporciona una manera consistente de registrar eventos, errores y debugging
en toda la aplicación.

Los logs se guardan en el directorio de datos del usuario (%LOCALAPPDATA%\\KGTracker\\logs),
con rotación automática. Si ese directorio no es escribible se usa la carpeta
temporal del sistema y, como último recurso, solo consola: el logger nunca
debe impedir que la aplicación arranque.

Nivel por defecto: INFO. Para depurar, definir la variable de entorno KGT_DEBUG=1.

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
from logging.handlers import RotatingFileHandler

LOG_NOMBRE = "kgametracker.log"
LOG_MAX_BYTES = 1_000_000
LOG_BACKUPS = 3


def _resolver_directorio_logs():
    """Devuelve un directorio de logs escribible, o None si no hay ninguno."""
    candidatos = []
    try:
        from core.paths import LOGS_DIR as _LOGS_USUARIO
        candidatos.append(str(_LOGS_USUARIO))
    except Exception:
        pass
    candidatos.append(os.path.join(tempfile.gettempdir(), "KGTracker", "logs"))

    for directorio in candidatos:
        try:
            os.makedirs(directorio, exist_ok=True)
            prueba = os.path.join(directorio, ".write_test")
            with open(prueba, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(prueba)
            return directorio
        except OSError:
            continue
    return None


LOGS_DIR = _resolver_directorio_logs()
LOG_FILE = os.path.join(LOGS_DIR, LOG_NOMBRE) if LOGS_DIR else None

_handlers = []
if LOG_FILE:
    try:
        _handlers.append(
            RotatingFileHandler(
                LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUPS, encoding="utf-8"
            )
        )
    except OSError:
        LOG_FILE = None

# El handler de consola solo si hay una consola real conectada (sys.stderr no es
# None). En un build sin consola (PyInstaller --noconsole / pythonw.exe)
# StreamHandler() usaría sys.stderr=None y cualquier log lanzaría una excepción.
if sys.stderr is not None:
    _handlers.append(logging.StreamHandler())
if not _handlers:
    _handlers.append(logging.NullHandler())

_NIVEL = logging.DEBUG if os.environ.get("KGT_DEBUG") == "1" else logging.INFO

logging.basicConfig(
    level=_NIVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=_handlers,
)

# Las librerías HTTP en DEBUG registran URLs completas; las mantenemos en WARNING.
for _nombre in ("urllib3", "requests", "PIL"):
    logging.getLogger(_nombre).setLevel(logging.WARNING)

# Obtener logger específico
logger = logging.getLogger("KGameTracker")


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
    return LOG_FILE or ""


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