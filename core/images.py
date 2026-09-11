import os

_REFERENCIAS_IMAGENES = {}


def limpiar_cache_imagenes():
    """Libera las referencias de miniaturas en memoria.

    No elimina los archivos PNG almacenados en disco.
    """
    _REFERENCIAS_IMAGENES.clear()
