"""
scripts/clean_release.py
Script de limpieza automatizada para preparar el repositorio antes de compilar/distribuir.
Elimina node_modules, cachés, archivos temporales y artefactos no deseados (REL-01).
"""

import os
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DIRECTORIOS_A_ELIMINAR = [
    "node_modules",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "tmp",
]

PATRONES_ARCHIVOS_A_ELIMINAR = [
    "*.tmp",
    "*.pyc",
    "*.pyo",
]


def limpiar():
    print("🧹 Iniciando limpieza de artefactos para distribución...")
    eliminados_count = 0

    # 1. Eliminar directorios pesados/desarrollo
    # Solo limpiar directorios conocidos en la raíz del proyecto; no borrar
    # subdirectorios o datos de usuario que casualmente compartan esos nombres.
    for nombre in DIRECTORIOS_A_ELIMINAR:
        item = ROOT_DIR / nombre
        if item.is_dir():
            try:
                shutil.rmtree(item)
                print(f"  [BORRADO] Directorio: {item.relative_to(ROOT_DIR)}")
                eliminados_count += 1
            except Exception as e:
                print(f"  [ERROR] No se pudo borrar {item}: {e}")

    # 2. Eliminar archivos temporales por patrón
    for patron in PATRONES_ARCHIVOS_A_ELIMINAR:
        for file_path in ROOT_DIR.rglob(patron):
            if file_path.is_file():
                if ".bak" in file_path.name.lower():
                    continue
                try:
                    file_path.unlink()
                    print(f"  [BORRADO] Archivo: {file_path.relative_to(ROOT_DIR)}")
                    eliminados_count += 1
                except Exception as e:
                    print(f"  [ERROR] No se pudo borrar {file_path}: {e}")

    print(f"✅ Limpieza completada. {eliminados_count} elementos borrados.")


if __name__ == "__main__":
    limpiar()
