# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.building.datastruct import TOC

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# The build host may expose Poppler's ICU DLLs through PATH. They are not the
# ICU implementation expected by the system Qt build and shadow Windows' ICU,
# causing QtCore to fail with WinError 127. Let Qt resolve the OS ICU instead.
incompatible_icu_dlls = {'icuuc.dll', 'icudt78.dll'}
a.binaries = TOC(
    entry for entry in a.binaries
    if Path(entry[0]).name.casefold() not in incompatible_icu_dlls
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KG-TRACKER',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icons/KGLogo.ico'],
)
