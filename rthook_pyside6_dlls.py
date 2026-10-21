"""Make the bundled Qt and Shiboken DLLs visible before importing PySide6."""

import os
import sys


if sys.platform == "win32" and getattr(sys, "frozen", False):
    bundle_root = sys._MEIPASS
    pyside_dir = os.path.join(bundle_root, "PySide6")
    shiboken_dir = os.path.join(bundle_root, "shiboken6")

    for dll_dir in (pyside_dir, shiboken_dir, bundle_root):
        if os.path.isdir(dll_dir):
            os.add_dll_directory(dll_dir)

    os.environ["PATH"] = os.pathsep.join(
        (pyside_dir, shiboken_dir, bundle_root, os.environ.get("PATH", ""))
    )
