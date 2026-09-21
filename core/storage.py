import os
import json
import time
import logging
from config import BASE_DIR

logger = logging.getLogger("KGTracker")

def guardar_json_atomico(ruta_archivo: str, datos: dict) -> bool:
    """
    Guarda datos de forma atomica (.tmp + fsync + os.replace) con tolerancia
    a bloqueos transitorios en Windows NTFS.
    """
    ruta_tmp = f"{ruta_archivo}.tmp"
    ruta_bak = f"{ruta_archivo}.bak"
    directorio = os.path.dirname(ruta_archivo)

    if directorio:
        os.makedirs(directorio, exist_ok=True)

    try:
        with open(ruta_tmp, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())

        # Backup preventivo
        if os.path.exists(ruta_archivo):
            try:
                import shutil
                shutil.copy2(ruta_archivo, ruta_bak)
            except Exception:
                pass

        # Reemplazo con reintentos para evitar PermissionError en Windows
        reintentos = 5
        demora = 0.05
        for intento in range(reintentos):
            try:
                os.replace(ruta_tmp, ruta_archivo)
                return True
            except (PermissionError, OSError) as e:
                if intento == reintentos - 1:
                    logger.error(f"Error al reemplazar {ruta_archivo} tras reintentos: {e}")
                    raise
                time.sleep(demora)
                demora *= 2

    except Exception as e:
        logger.error(f"Fallo en guardado atomico de {ruta_archivo}: {e}")
        if os.path.exists(ruta_tmp):
            try:
                os.remove(ruta_tmp)
            except OSError:
                pass
        return False

def cargar_json_seguro(ruta_archivo: str, default: dict = None, valor_por_defecto: dict = None) -> dict:
    """
    Carga un JSON de disco; si falla o esta corrupto, intenta recuperar el .bak.
    Soporta tanto 'default' como 'valor_por_defecto'.
    """
    if valor_por_defecto is not None:
        default_val = valor_por_defecto
    elif default is not None:
        default_val = default
    else:
        default_val = {}

    target = ruta_archivo
    if not os.path.exists(target):
        bak = f"{ruta_archivo}.bak"
        if os.path.exists(bak):
            target = bak
        else:
            return default_val

    try:
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Archivo no legible {target}: {e}. Intentando .bak...")
        bak = f"{ruta_archivo}.bak"
        if target != bak and os.path.exists(bak):
            try:
                with open(bak, "r", encoding="utf-8") as fb:
                    return json.load(fb)
            except Exception as eb:
                logger.error(f"Fallo critico al leer backup {bak}: {eb}")
        return default_val

# Alias de compatibilidad
guardar_datos_atomicos = guardar_json_atomico
cargar_datos_seguros = cargar_json_seguro
