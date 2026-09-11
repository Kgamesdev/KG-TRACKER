import json
import os
import shutil

def guardar_json_atomico(ruta_archivo, datos):
    """
    Guarda datos JSON de forma atómica.
    Escribe primero en un archivo temporal y luego renombra.
    Evita la corrupción del archivo en caso de corte o cierre inesperado.
    """
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    ruta_tmp = f"{ruta_archivo}.tmp"
    ruta_bak = f"{ruta_archivo}.bak"

    try:
        # Guardar en archivo temporal
        with open(ruta_tmp, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())

        # Si el archivo original ya existía, conservar respaldo
        if os.path.exists(ruta_archivo):
            shutil.copy2(ruta_archivo, ruta_bak)

        # Reemplazo atómico (en Windows os.replace es atómico)
        os.replace(ruta_tmp, ruta_archivo)
        return True

    except Exception as e:
        if os.path.exists(ruta_tmp):
            try:
                os.remove(ruta_tmp)
            except Exception:
                pass
        raise e


def cargar_json_seguro(ruta_archivo, valor_por_defecto=None):
    """
    Carga un archivo JSON. Si está corrupto, intenta rescatar desde el .bak.
    """
    if valor_por_defecto is None:
        valor_por_defecto = []

    if not os.path.exists(ruta_archivo):
        return valor_por_defecto

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        ruta_bak = f"{ruta_archivo}.bak"
        if os.path.exists(ruta_bak):
            try:
                with open(ruta_bak, "r", encoding="utf-8") as fb:
                    return json.load(fb)
            except Exception:
                pass
        return valor_por_defecto
