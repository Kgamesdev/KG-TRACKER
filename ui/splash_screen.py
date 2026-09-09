"""Splash de KG TRACKER usando el logo maestro con alfa real por píxel en Windows.

No usa chroma key, transparentcolor ni sombra externa.
La animación está ajustada a unos 4 segundos, con entrada y salida suaves.
"""

import ctypes
from ctypes import wintypes
import os
import tkinter as tk

from PIL import Image
from config import COLOR_BG, LOGO_PATH, SPLASH_MAX_WIDTH

# ---- Animación original ----
DURACION_ENTRADA_MS = 500
DURACION_ESPERA_MS = 3000
DURACION_SALIDA_MS = 500
INTERVALO_FRAME_MS = 8
ESCALA_INICIAL = 1.0

if os.name == "nt":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)

    LRESULT = ctypes.c_ssize_t

    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

    class SIZE(ctypes.Structure):
        _fields_ = [("cx", wintypes.LONG), ("cy", wintypes.LONG)]

    class BLENDFUNCTION(ctypes.Structure):
        _fields_ = [
            ("BlendOp", wintypes.BYTE),
            ("BlendFlags", wintypes.BYTE),
            ("SourceConstantAlpha", wintypes.BYTE),
            ("AlphaFormat", wintypes.BYTE),
        ]

    WNDPROC = ctypes.WINFUNCTYPE(
        LRESULT,
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM,
    )

    class WNDCLASSW(ctypes.Structure):
        _fields_ = [
            ("style", wintypes.UINT),
            ("lpfnWndProc", WNDPROC),
            ("cbClsExtra", ctypes.c_int),
            ("cbWndExtra", ctypes.c_int),
            ("hInstance", wintypes.HINSTANCE),
            ("hIcon", wintypes.HICON),
            ("hCursor", wintypes.HCURSOR),
            ("hbrBackground", wintypes.HBRUSH),
            ("lpszMenuName", wintypes.LPCWSTR),
            ("lpszClassName", wintypes.LPCWSTR),
        ]

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", wintypes.DWORD),
            ("biWidth", wintypes.LONG),
            ("biHeight", wintypes.LONG),
            ("biPlanes", wintypes.WORD),
            ("biBitCount", wintypes.WORD),
            ("biCompression", wintypes.DWORD),
            ("biSizeImage", wintypes.DWORD),
            ("biXPelsPerMeter", wintypes.LONG),
            ("biYPelsPerMeter", wintypes.LONG),
            ("biClrUsed", wintypes.DWORD),
            ("biClrImportant", wintypes.DWORD),
        ]

    class BITMAPINFO(ctypes.Structure):
        _fields_ = [
            ("bmiHeader", BITMAPINFOHEADER),
            ("bmiColors", wintypes.DWORD * 1),
        ]

    # Win32 constants
    WS_POPUP = 0x80000000
    WS_EX_LAYERED = 0x00080000
    WS_EX_TOOLWINDOW = 0x00000080
    WS_EX_TOPMOST = 0x00000008
    WS_EX_NOACTIVATE = 0x08000000
    SW_SHOWNOACTIVATE = 4
    HWND_TOPMOST = wintypes.HWND(-1)
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_NOACTIVATE = 0x0010
    SWP_SHOWWINDOW = 0x0040
    ULW_ALPHA = 0x00000002
    AC_SRC_ALPHA = 0x01
    BI_RGB = 0
    DIB_RGB_COLORS = 0
    WM_NCHITTEST = 0x0084
    HTTRANSPARENT = -1

    user32.DefWindowProcW.argtypes = [
        wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
    ]
    user32.DefWindowProcW.restype = LRESULT

    user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
    user32.RegisterClassW.restype = wintypes.ATOM

    kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    kernel32.GetModuleHandleW.restype = wintypes.HMODULE

    user32.CreateWindowExW.argtypes = [
        wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
        wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.c_int, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE,
        wintypes.LPVOID,
    ]
    user32.CreateWindowExW.restype = wintypes.HWND

    user32.DestroyWindow.argtypes = [wintypes.HWND]
    user32.DestroyWindow.restype = wintypes.BOOL

    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.ShowWindow.restype = wintypes.BOOL

    user32.SetWindowPos.argtypes = [
        wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int,
        ctypes.c_int, ctypes.c_int, wintypes.UINT
    ]
    user32.SetWindowPos.restype = wintypes.BOOL

    user32.UpdateLayeredWindow.argtypes = [
        wintypes.HWND, wintypes.HDC, ctypes.POINTER(POINT),
        ctypes.POINTER(SIZE), wintypes.HDC, ctypes.POINTER(POINT),
        wintypes.COLORREF, ctypes.POINTER(BLENDFUNCTION), wintypes.DWORD
    ]
    user32.UpdateLayeredWindow.restype = wintypes.BOOL

    user32.GetDC.argtypes = [wintypes.HWND]
    user32.GetDC.restype = wintypes.HDC
    user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    user32.ReleaseDC.restype = ctypes.c_int

    gdi32.CreateCompatibleDC.argtypes = [wintypes.HDC]
    gdi32.CreateCompatibleDC.restype = wintypes.HDC

    gdi32.DeleteDC.argtypes = [wintypes.HDC]
    gdi32.DeleteDC.restype = wintypes.BOOL

    gdi32.CreateDIBSection.argtypes = [
        wintypes.HDC, ctypes.POINTER(BITMAPINFO), wintypes.UINT,
        ctypes.POINTER(ctypes.c_void_p), wintypes.HANDLE, wintypes.DWORD
    ]
    gdi32.CreateDIBSection.restype = wintypes.HBITMAP

    gdi32.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
    gdi32.SelectObject.restype = wintypes.HGDIOBJ

    gdi32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
    gdi32.DeleteObject.restype = wintypes.BOOL

    _WNDPROC = None
    _CLASS_NAME = "KG_TRACKER_SPLASH_LAYERED_V1"

    def _wnd_proc(hwnd, msg, wparam, lparam):
        if msg == WM_NCHITTEST:
            return HTTRANSPARENT
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    _WNDPROC = WNDPROC(_wnd_proc)

    def _registrar_clase():
        hinstance = kernel32.GetModuleHandleW(None)
        wc = WNDCLASSW()
        wc.style = 0
        wc.lpfnWndProc = _WNDPROC
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = hinstance
        wc.hIcon = None
        wc.hCursor = None
        wc.hbrBackground = None
        wc.lpszMenuName = None
        wc.lpszClassName = _CLASS_NAME

        atom = user32.RegisterClassW(ctypes.byref(wc))
        if not atom:
            error = ctypes.get_last_error()
            # 1410 = clase ya registrada. Es válido.
            if error != 1410:
                raise ctypes.WinError(error)

    def _rgba_a_premultiplied_bgra(image):
        """Convierte RGBA a BGRA premultiplicado, necesario para ULW_ALPHA."""
        import numpy as np
        arr = np.asarray(image, dtype=np.uint8)
        rgb = arr[:, :, :3].astype(np.uint16)
        alpha = arr[:, :, 3].astype(np.uint16)
        premul = ((rgb * alpha[:, :, None] + 127) // 255).astype(np.uint8)
        bgra = np.empty_like(arr)
        bgra[:, :, 0] = premul[:, :, 2]
        bgra[:, :, 1] = premul[:, :, 1]
        bgra[:, :, 2] = premul[:, :, 0]
        bgra[:, :, 3] = alpha.astype(np.uint8)
        return bgra.tobytes()

    def _actualizar_ventana(hwnd, image, x, y):
        width, height = image.size
        pixels = _rgba_a_premultiplied_bgra(image)

        screen_dc = user32.GetDC(None)
        if not screen_dc:
            raise ctypes.WinError(ctypes.get_last_error())

        mem_dc = gdi32.CreateCompatibleDC(screen_dc)
        if not mem_dc:
            user32.ReleaseDC(None, screen_dc)
            raise ctypes.WinError(ctypes.get_last_error())

        bits = ctypes.c_void_p()
        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height  # top-down
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = BI_RGB

        bitmap = gdi32.CreateDIBSection(
            screen_dc,
            ctypes.byref(bmi),
            DIB_RGB_COLORS,
            ctypes.byref(bits),
            None,
            0,
        )
        if not bitmap or not bits.value:
            gdi32.DeleteDC(mem_dc)
            user32.ReleaseDC(None, screen_dc)
            raise ctypes.WinError(ctypes.get_last_error())

        old_bitmap = gdi32.SelectObject(mem_dc, bitmap)
        try:
            ctypes.memmove(bits.value, pixels, len(pixels))

            dst = POINT(x, y)
            size = SIZE(width, height)
            src = POINT(0, 0)
            blend = BLENDFUNCTION(0, 0, 255, AC_SRC_ALPHA)

            ok = user32.UpdateLayeredWindow(
                hwnd, screen_dc, ctypes.byref(dst), ctypes.byref(size),
                mem_dc, ctypes.byref(src), 0, ctypes.byref(blend), ULW_ALPHA
            )
            if not ok:
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            gdi32.SelectObject(mem_dc, old_bitmap)
            gdi32.DeleteObject(bitmap)
            gdi32.DeleteDC(mem_dc)
            user32.ReleaseDC(None, screen_dc)


class _NativeSplash:
    def __init__(self, root, logo):
        self.root = root
        self.logo = logo
        self.hwnd = None
        self._x = 0
        self._y = 0
        self._create()

    def _create(self):
        _registrar_clase()
        self.width, self.height = self.logo.size
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self._x = (sw - self.width) // 2
        self._y = (sh - self.height) // 2

        hinstance = kernel32.GetModuleHandleW(None)
        hwnd = user32.CreateWindowExW(
            WS_EX_LAYERED | WS_EX_TOOLWINDOW | WS_EX_TOPMOST | WS_EX_NOACTIVATE,
            _CLASS_NAME,
            "",
            WS_POPUP,
            self._x, self._y, self.width, self.height,
            None, None, hinstance, None
        )
        if not hwnd:
            raise ctypes.WinError(ctypes.get_last_error())

        self.hwnd = hwnd
        user32.ShowWindow(self.hwnd, SW_SHOWNOACTIVATE)
        user32.SetWindowPos(
            self.hwnd, HWND_TOPMOST,
            self._x, self._y, self.width, self.height,
            SWP_NOACTIVATE | SWP_SHOWWINDOW
        )

    def render(self, image):
        _actualizar_ventana(self.hwnd, image, self._x, self._y)

    def destroy(self):
        if self.hwnd:
            try:
                user32.DestroyWindow(self.hwnd)
            finally:
                self.hwnd = None


def _ease_smooth(t):
    """Transición suave sin tirón al principio ni al final."""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def _preparar_logo():
    logo = Image.open(LOGO_PATH).convert("RGBA")

    # El PNG maestro ya contiene exactamente la forma y el alfa deseados.
    # Solo se reduce manteniendo el alfa; no se añade fondo ni sombra.
    if logo.width > SPLASH_MAX_WIDTH:
        ratio = SPLASH_MAX_WIDTH / float(logo.width)
        logo = logo.resize(
            (SPLASH_MAX_WIDTH, max(1, int(logo.height * ratio))),
            Image.Resampling.LANCZOS,
        )
    return logo


def mostrar_splash_inicio(root, al_terminar):
    """Muestra el logo maestro con transparencia alfa real y la animación original."""

    if os.name != "nt":
        # Fallback simple para sistemas no Windows.
        splash = tk.Toplevel(root)
        splash.overrideredirect(True)
        splash.configure(bg=COLOR_BG)
        logo = _preparar_logo()
        from PIL import ImageTk
        foto = ImageTk.PhotoImage(logo)
        label = tk.Label(splash, image=foto, bg=COLOR_BG, bd=0)
        label.image = foto
        label.pack()
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() - logo.width) // 2
        y = (splash.winfo_screenheight() - logo.height) // 2
        splash.geometry(f"{logo.width}x{logo.height}+{x}+{y}")
        splash.after(DURACION_ESPERA_MS, lambda: (splash.destroy(), al_terminar()))
        return

    try:
        logo_base = _preparar_logo()
        splash = _NativeSplash(root, logo_base)
    except Exception as e:
        print(f"⚠️ Splash nativo no disponible: {e}")
        al_terminar()
        return

    pasos_entrada = max(1, DURACION_ENTRADA_MS // INTERVALO_FRAME_MS)
    pasos_salida = max(1, DURACION_SALIDA_MS // INTERVALO_FRAME_MS)

    def renderizar(alpha_frac, escala_frac=None):
        # El tamaño y la posición de la ventana permanecen FIJOS durante toda
        # la animación. Solo cambia el alfa del logo; así no hay vibración,
        # reescalado ni pequeños saltos de posición.
        frame = logo_base.copy()

        if alpha_frac < 0.999:
            alpha = frame.getchannel("A")
            alpha = alpha.point(lambda p: int(p * alpha_frac))
            frame.putalpha(alpha)

        splash.render(frame)

    def finalizar():
        splash.destroy()
        al_terminar()

    def animar_entrada(i=1):
        if not splash.hwnd:
            return
        t = _ease_smooth(i / float(pasos_entrada))
        renderizar(t)
        if i < pasos_entrada:
            root.after(INTERVALO_FRAME_MS, lambda: animar_entrada(i + 1))
        else:
            root.after(DURACION_ESPERA_MS, animar_salida)

    def animar_salida(i=1):
        if not splash.hwnd:
            finalizar()
            return
        t = _ease_smooth(i / float(pasos_salida))
        renderizar(1 - t)
        if i < pasos_salida:
            root.after(INTERVALO_FRAME_MS, lambda: animar_salida(i + 1))
        else:
            finalizar()

    renderizar(0.0, 0.0)
    root.after(8, animar_entrada)
