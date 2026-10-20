"""
build.py
Script maestro de compilación automatizada y verificable para KG Tracker.
Proceso: Limpieza -> Tests -> Compilación PyInstaller -> Checksum SHA256.
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def ejecutar_comando(cmd: list, descripcion: str) -> bool:
    print(f"\n🔄 [{descripcion}] Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    if result.returncode != 0:
        print(f"❌ [{descripcion}] FALLÓ con código de salida {result.returncode}")
        return False
    print(f"✅ [{descripcion}] COMPLETADO con éxito.")
    return True


def calcular_sha256(filepath: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():
    print("==================================================")
    print("🚀 KG TRACKER — PIPELINE DE COMPILACIÓN DE RELEASE")
    print("==================================================")

    # 1. Limpieza omitida intencionadamente.
    # No ejecutar clean_release.py hasta revisar y corregir su comportamiento destructivo.

    # 2. Ejecutar la suite completa de tests
    print("\n🧪 Ejecutando suite de pruebas unitarias e integración...")
    if not ejecutar_comando([sys.executable, "-m", "unittest", "discover", "-s", "tests"], "SUITE DE TESTS"):
        print("🛑 Compilación abortada: Los tests fallaron.")
        sys.exit(1)

    # 3. Compilar ejecutable con PyInstaller
    spec_file = ROOT_DIR / "KG-TRACKER.spec"
    if not spec_file.exists():
        print(f"❌ Error: No se encontró el archivo spec {spec_file}")
        sys.exit(1)

    if not ejecutar_comando([sys.executable, "-m", "PyInstaller", "--noconfirm", str(spec_file)], "COMPILACIÓN PYINSTALLER"):
        sys.exit(1)

    # 4. Verificar ejecutable generado y calcular checksum SHA256
    exe_path = ROOT_DIR / "dist" / "KG-TRACKER.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        checksum = calcular_sha256(exe_path)

        checksum_file = ROOT_DIR / "dist" / "KG-TRACKER.exe.sha256"
        checksum_file.write_text(f"{checksum}  KG-TRACKER.exe\n", encoding="utf-8")

        print("\n==================================================")
        print("🎉 COMPILACIÓN EXITOSA — RESUMEN DE RELEASE")
        print("==================================================")
        print(f"📦 Ubicación: {exe_path}")
        print(f"📏 Tamaño: {size_mb:.2f} MB")
        print(f"🔑 SHA256: {checksum}")
        print(f"📄 Checksum guardado en: {checksum_file}")
        print("==================================================")
    else:
        print("❌ Error: El ejecutable dist/KG-TRACKER.exe no fue generado.")
        sys.exit(1)


if __name__ == "__main__":
    main()
