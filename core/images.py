import os
import time
from core.paths import CACHE_DIR

_REFERENCIAS_IMAGENES = {}


def limpiar_cache_imagenes(limpiar_disco: bool = False) -> None:
    _REFERENCIAS_IMAGENES.clear()
    if limpiar_disco:
        limpiar_cache_disco()


def limpiar_cache_disco(dias_max: int = 14, max_archivos: int = 500) -> int:
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

        if len(entradas_restantes) > max_archivos:
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
        pass

    return archivos_eliminados
