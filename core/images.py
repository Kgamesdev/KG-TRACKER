import os
import time
from config import BASE_DIR

_REFERENCIAS_IMAGENES = {}
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def limpiar_cache_imagenes(limpiar_disco: bool = False) -> None:
    """Libera las referencias de miniaturas en memoria RAM.
    
    Si limpiar_disco=True, ejecuta tambien la purga TTL de archivos viejos.
    """
    _REFERENCIAS_IMAGENES.clear()
    if limpiar_disco:
        limpiar_cache_disco()


def limpiar_cache_disco(dias_max: int = 14, max_archivos: int = 500) -> int:
    """Purga de forma defensiva las imagenes en cache mas antiguas que dias_max
    o si se excede max_archivos (politica LRU basada en mtime).
    
    Retorna el numero de archivos eliminados.
    Nunca propaga excepciones a la UI.
    """
    if not os.path.exists(CACHE_DIR):
        return 0

    archivos_eliminados = 0
    ahora = time.time()
    segundos_max = dias_max * 86400

    try:
        entradas = []
        for entrada in os.scandir(CACHE_DIR):
            if entrada.is_file() and entrada.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                try:
                    stat = entrada.stat()
                    entradas.append((entrada.path, stat.st_mtime))
                except (OSError, PermissionError):
                    continue

        # 1. Purgar archivos que superen el TTL
        entradas_restantes = []
        for ruta, mtime in entradas:
            if ahora - mtime > segundos_max:
                try:
                    os.remove(ruta)
                    archivos_eliminados += 1
                except (OSError, PermissionError):
                    entradas_restantes.append((ruta, mtime))
            else:
                entradas_restantes.append((ruta, mtime))

        # 2. Si todavia superamos el maximo permitido, eliminar los mas viejos primero (LRU)
        if len(entradas_restantes) > max_archivos:
            # Ordenar por fecha de modificacion ascendente (mas viejos primero)
            entradas_restantes.sort(key=lambda x: x[1])
            exceso = len(entradas_restantes) - max_archivos
            for i in range(exceso):
                ruta = entradas_restantes[i][0]
                try:
                    os.remove(ruta)
                    archivos_eliminados += 1
                except (OSError, PermissionError):
                    pass

    except Exception:
        # Falla de forma totalmente silenciosa para garantizar estabilidad
        pass

    return archivos_eliminados
