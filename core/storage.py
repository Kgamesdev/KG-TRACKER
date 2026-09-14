import json
import os
import shutil
from pathlib import Path

from core.paths import (
    SETTINGS_FILE,
    RECLAMADOS_FILE,
    CACHE_GIVEAWAYS_FILE,
    migrar_datos_desarrollo_si_existen
)

# Migrar automáticamente archivos de 'data/' si existen de una versión previa
migrar_datos_desarrollo_si_existen()


def guardar_json_atomico(ruta_archivo, datos):
    """
    Guarda datos JSON de forma atómica.
    Escribe primero en un archivo temporal (.tmp), realiza fsync y luego renombra (os.replace).
    Evita la corrupción del archivo en caso de corte o cierre inesperado.
    """
    ruta_archivo = Path(ruta_archivo)
    directorio = ruta_archivo.parent
    directorio.mkdir(parents=True, exist_ok=True)

    ruta_tmp = Path(f"{ruta_archivo}.tmp")
    ruta_bak = Path(f"{ruta_archivo}.bak")

    try:
        with open(ruta_tmp, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())

        if ruta_archivo.exists():
            shutil.copy2(ruta_archivo, ruta_bak)

        os.replace(ruta_tmp, ruta_archivo)
        return True

    except Exception as e:
        if ruta_tmp.exists():
            try:
                ruta_tmp.unlink()
            except Exception:
                pass
        raise e


def cargar_json_seguro(ruta_archivo, valor_por_defecto=None):
    """
    Carga un archivo JSON. Si está corrupto o no existe, intenta rescatar desde el .bak.
    """
    if valor_por_defecto is None:
        valor_por_defecto = []

    ruta_archivo = Path(ruta_archivo)
    ruta_bak = Path(f"{ruta_archivo}.bak")

    for target in (ruta_archivo, ruta_bak):
        if target.exists():
            try:
                with open(target, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    return valor_por_defecto
