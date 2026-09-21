# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE

block_cipher = None

# Mapear carpeta de assets de solo lectura
datas = [
    ('assets', 'assets'),
]

hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'core.paths',
    'core.storage',
    'core.tray',
    'core.validators',
    'core.network',
    'core.image_loader',
    'core.ui_settings',
    'ui.design_system',
]

# Exclusiones de modulos pesados no utilizados para reducir el tamano del ejecutable (-200MB+)
excludes = [
    # Modulos pesados no utilizados de PySide6 / Qt6
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebEngineQuick',
    'PySide6.QtQuick',
    'PySide6.QtQuick3D',
    'PySide6.QtQuickControls2',
    'PySide6.QtQml',
    'PySide6.QtDesigner',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DRender',
    'PySide6.Qt3DAnimation',
    'PySide6.Qt3DInput',
    'PySide6.Qt3DLogic',
    'PySide6.Qt3DExtras',
    'PySide6.QtCharts',
    'PySide6.QtDataVisualization',
    'PySide6.QtGraphs',
    'PySide6.QtLocation',
    'PySide6.QtPositioning',
    'PySide6.QtSensors',
    'PySide6.QtSerialBus',
    'PySide6.QtSerialPort',
    'PySide6.QtSpatialAudio',
    'PySide6.QtVirtualKeyboard',
    'PySide6.QtBluetooth',
    'PySide6.QtNfc',
    'PySide6.QtScxml',
    'PySide6.QtRemoteObjects',
    'PySide6.QtPdf',
    'PySide6.QtPdfWidgets',
    'PySide6.QtHttpServer',
    'PySide6.QtTest',
    # Modulos de desarrollo y testing de Python
    'node_modules',
    'tkinter',
    'unittest',
    'pydoc',
    'doctest',
    'test',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KGameTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana CMD de consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo.ico' if os.path.exists('assets/logo.ico') else None,
)
