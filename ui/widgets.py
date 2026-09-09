from PIL import Image, ImageTk
import os
"""Widgets reutilizables para la interfaz gráfica.

Nota: Este módulo contiene componentes que pueden usarse
en futuras versiones. Actualmente, la lógica está en main_window.py
"""

import webbrowser
import tkinter as tk
from tkinter import ttk

from config import (
    COLOR_BORDER,
    COLOR_BG, COLOR_BG_CARD, COLOR_BG_DESC,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT,
    COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
)
from core.images import descargar_imagen_thumbnail, guardar_en_cache


def abrir_enlace(url):
    """Abre un enlace en el navegador predeterminado."""
    if url:
        webbrowser.open(url)


def crear_seccion_tienda(parent, nombre_tienda, lista_juegos, callback_enlace=None):
    """
    Crea una sección acordeón para una tienda con sus juegos.
    
    Args:
        parent (tk.Widget): Widget padre
        nombre_tienda (str): Nombre de la tienda (ej: "Steam", "Epic Games")
        lista_juegos (list): Lista de diccionarios con datos de juegos
        callback_enlace (callable): Función a llamar cuando se haga click en "Reclamar"
        
    Returns:
        tk.Frame: Frame contenedor de la sección
        
    Ejemplo:
        seccion = crear_seccion_tienda(
            parent_frame,
            "Steam",
            lista_juegos_steam,
            callback_enlace=webbrowser.open
        )
    """
    store_container = tk.Frame(parent, bg=COLOR_BG)
    store_container.pack(fill="x", pady=(8, 4))

    # Frame que contendrá los juegos
    content_games_frame = tk.Frame(store_container, bg=COLOR_BG)
    
    # Variable para controlar si está expandido
    is_expanded = tk.BooleanVar(value=True)

    def crear_toggle(btn, frame, var, nombre, cantidad):
        """Crea la función de toggle para expandir/contraer."""
        def toggle():
            if var.get():
                frame.pack_forget()
                var.set(False)
                btn.config(text=f"▶ 🏪 {nombre} ({cantidad} juegos)")
            else:
                frame.pack(fill="x", expand=True, pady=(4, 0))
                var.set(True)
                btn.config(text=f"▼ 🏪 {nombre} ({cantidad} juegos)")
        return toggle

    # Botón header (expandir/contraer)
    btn_seccion = tk.Button(
        store_container,
        text=f"▼ 🏪 {nombre_tienda} ({len(lista_juegos)} juegos)",
        font=("Arial", 11, "bold"),
        bg=COLOR_BG,
        fg=COLOR_ACCENT,
        activebackground=COLOR_BG,
        activeforeground=COLOR_ACCENT_LIGHT,
        relief="flat",
        anchor="w",
        cursor="hand2"
    )
    btn_seccion.config(
        command=crear_toggle(
            btn_seccion,
            content_games_frame,
            is_expanded,
            nombre_tienda,
            len(lista_juegos)
        )
    )
    btn_seccion.pack(fill="x")

    # Frame con los juegos
    content_games_frame.pack(fill="x", expand=True, pady=(4, 0))

    # Crear tarjetas para cada juego
    for juego in lista_juegos:
        crear_tarjeta_juego(
            content_games_frame,
            juego,
            nombre_tienda,
            callback_enlace=callback_enlace
        )

    return store_container


def crear_tarjeta_juego(parent, juego, nombre_tienda, callback_enlace=None):
    """
    Crea una tarjeta individual de un juego.
    
    Args:
        parent (tk.Widget): Widget padre
        juego (dict): Diccionario con datos del juego:
            - title: Nombre del juego
            - image: URL de la imagen
            - open_giveaway_url: URL para reclamar
            - description: Descripción
        nombre_tienda (str): Nombre de la tienda
        callback_enlace (callable): Función a llamar al hacer click en "Reclamar"
        
    Returns:
        tk.Frame: Frame contenedor de la tarjeta
        
    Ejemplo:
        card = crear_tarjeta_juego(
            lista_frame,
            juego_dict,
            "Steam",
            callback_enlace=webbrowser.open
        )
    """
    titulo = juego.get("title", "Elemento sin título")
    thumb_url = juego.get("image") or juego.get("thumbnail")
    link_url = juego.get("open_giveaway_url") or juego.get("worth")
    descripcion = juego.get("description", "Promoción de juego gratuito por tiempo limitado.")

    # Marco de la tarjeta
    card = tk.Frame(
        parent,
        bg=COLOR_BG_CARD,
        bd=1,
        relief="solid",
        padx=12,
        pady=10
    )
    card.pack(fill="x", pady=4)

    # Frame superior (imagen + info + botón)
    top_frame = tk.Frame(card, bg=COLOR_BG_CARD)
    top_frame.pack(fill="x", expand=True)

    # Descargar y mostrar imagen
    photo = descargar_imagen_thumbnail(thumb_url)
    if photo:
        guardar_en_cache(photo)
        lbl_img = tk.Label(top_frame, image=photo, bg=COLOR_BG_CARD)
        lbl_img.pack(side="left", padx=(0, 10))

    # Frame de información (título, tienda)
    info_frame = tk.Frame(top_frame, bg=COLOR_BG_CARD)
    info_frame.pack(side="left", fill="x", expand=True)

    # Título del juego
    lbl_titulo_juego = tk.Label(
        info_frame,
        text=titulo,
        font=("Arial", 11, "bold"),
        bg=COLOR_BG_CARD,
        fg=COLOR_TEXT_PRIMARY,
        anchor="w",
        wraplength=220,
        justify="left"
    )
    lbl_titulo_juego.pack(fill="x")

    # Nombre de la tienda
    lbl_tienda_juego = tk.Label(
        info_frame,
        text=f"🏪 {nombre_tienda}",
        font=("Arial", 8, "bold"),
        bg=COLOR_BG_CARD,
        fg=COLOR_ACCENT,
        anchor="w"
    )
    lbl_tienda_juego.pack(fill="x")

    # Botón Reclamar
    def on_click_reclamar():
        if callback_enlace:
            callback_enlace(link_url)
        else:
            abrir_enlace(link_url)

    btn_reclamar = tk.Button(
        top_frame,
        text="🚀 Reclamar",
        font=("Arial", 9, "bold"),
        bg=COLOR_SUCCESS,
        fg="white",
        activebackground=COLOR_SUCCESS_HOVER,
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2",
        command=on_click_reclamar
    )
    btn_reclamar.pack(side="right", padx=5)

    # Descripción (en la parte inferior)
    descripcion_truncada = descripcion[:120] + "..." if len(descripcion) > 120 else descripcion
    lbl_sinopsis = tk.Label(
        card,
        text=f"📝 {descripcion_truncada}",
        font=("Arial", 8, "italic"),
        bg=COLOR_BG_DESC,
        fg=COLOR_TEXT_MUTED,
        anchor="w",
        wraplength=480,
        justify="left",
        padx=8,
        pady=4
    )
    lbl_sinopsis.pack(fill="x", pady=(8, 0))

    return card


def crear_boton_custom(parent, texto, comando, estilo="accent"):
    """
    Crea un botón personalizado con estilos predefinidos.
    
    Args:
        parent (tk.Widget): Widget padre
        texto (str): Texto del botón
        comando (callable): Función a ejecutar al hacer click
        estilo (str): "accent", "success", "error", "muted"
        
    Returns:
        tk.Button: El botón creado
        
    Ejemplo:
        btn = crear_boton_custom(frame, "Buscar", mi_funcion, estilo="accent")
    """
    estilos = {
        "accent": {
            "bg": COLOR_ACCENT,
            "fg": "white",
            "activebackground": COLOR_ACCENT_HOVER,
        },
        "success": {
            "bg": COLOR_SUCCESS,
            "fg": "white",
            "activebackground": COLOR_SUCCESS_HOVER,
        },
        "error": {
            "bg": "#EF4444",
            "fg": "white",
            "activebackground": "#DC2626",
        },
        "muted": {
            "bg": COLOR_BG_CARD,
            "fg": COLOR_TEXT_SECONDARY,
            "activebackground": COLOR_BG,
        }
    }

    config = estilos.get(estilo, estilos["accent"])

    btn = tk.Button(
        parent,
        text=texto,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=6,
        cursor="hand2",
        command=comando,
        **config
    )

    return btn


class RoundedButton(tk.Frame):
    """Botón con esquinas redondeadas y soporte para icono PNG."""

    def __init__(
        self,
        parent,
        text="",
        command=None,
        width=120,
        height=42,
        bg="#2D2D3F",
        hover_bg="#38384D",
        fg="white",
        radius=12,
        font=("Segoe UI", 9, "bold"),
        border=COLOR_BORDER,
        border_width=1,
        icon_path=None,
        icon_size=(20, 20),
        **kwargs
    ):
        super().__init__(parent, bg=parent.cget("bg"), bd=0, highlightthickness=0, **kwargs)
        self._bg = bg
        self._hover = hover_bg
        self._fg = fg
        self._border = border
        self._border_width = border_width
        self._radius = radius
        self._command = command
        self._width = width
        self._height = height
        self._font = font
        self._icon_path = icon_path
        self._icon_size = icon_size
        self._icon_photo = None

        self._canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            bd=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2"
        )
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", self._draw)
        self._canvas.bind("<Enter>", self._enter)
        self._canvas.bind("<Leave>", self._leave)
        self._canvas.bind("<Button-1>", self._click)
        self._text = text
        self._load_icon()
        self._draw()

    def _load_icon(self):
        self._icon_photo = None
        if not self._icon_path or not os.path.exists(self._icon_path):
            return
        try:
            img = Image.open(self._icon_path).convert("RGBA")
            img.thumbnail(self._icon_size, Image.Resampling.LANCZOS)
            self._icon_photo = ImageTk.PhotoImage(img)
        except Exception:
            self._icon_photo = None

    def set_icon(self, icon_path):
        self._icon_path = icon_path
        self._load_icon()
        self._draw()

    def _rounded_polygon(self, x1, y1, x2, y2, r):
        return [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]

    def _draw_contents(self):
        w = max(20, self._canvas.winfo_width())
        h = max(20, self._canvas.winfo_height())
        if self._icon_photo and self._text:
            text_width = max(1, len(self._text) * 6)
            total_width = self._icon_size[0] + 8 + text_width
            start_x = (w - total_width) / 2
            self._canvas.create_image(
                start_x + self._icon_size[0] / 2,
                h / 2,
                image=self._icon_photo
            )
            self._canvas.create_text(
                start_x + self._icon_size[0] + 8 + text_width / 2,
                h / 2,
                text=self._text,
                fill=self._fg,
                font=self._font,
                justify="center"
            )
        elif self._icon_photo:
            self._canvas.create_image(w / 2, h / 2, image=self._icon_photo)
        else:
            self._canvas.create_text(w / 2, h / 2, text=self._text, fill=self._fg, font=self._font, justify="center")

    def _draw(self, _event=None):
        self._canvas.delete("all")
        w = max(20, self._canvas.winfo_width())
        h = max(20, self._canvas.winfo_height())
        r = min(self._radius, w // 2, h // 2)
        self._canvas.create_polygon(
            self._rounded_polygon(1, 1, w - 1, h - 1, r),
            smooth=True,
            splinesteps=18,
            fill=self._bg,
            outline=self._border,
            width=self._border_width
        )
        self._draw_contents()

    def _enter(self, _event=None):
        self._canvas.delete("all")
        w = max(20, self._canvas.winfo_width())
        h = max(20, self._canvas.winfo_height())
        r = min(self._radius, w // 2, h // 2)
        self._canvas.create_polygon(
            self._rounded_polygon(1, 1, w - 1, h - 1, r),
            smooth=True,
            splinesteps=18,
            fill=self._hover,
            outline=self._border,
            width=self._border_width
        )
        self._draw_contents()

    def _leave(self, _event=None):
        self._draw()

    def _click(self, _event=None):
        if callable(self._command):
            self._command()

    def set_colors(self, bg=None, hover=None, fg=None, border=None):
        if bg is not None:
            self._bg = bg
        if hover is not None:
            self._hover = hover
        if fg is not None:
            self._fg = fg
        if border is not None:
            self._border = border
        self._draw()

    def config(self, **kwargs):
        if "text" in kwargs:
            self._text = kwargs.pop("text")
        if "bg" in kwargs:
            self._bg = kwargs.pop("bg")
        if "fg" in kwargs:
            self._fg = kwargs.pop("fg")
        if "activebackground" in kwargs:
            self._hover = kwargs.pop("activebackground")
        if "font" in kwargs:
            self._font = kwargs.pop("font")
        self._draw()
        if kwargs:
            super().config(**kwargs)

    configure = config



class VolumeSlider(tk.Frame):
    """Slider de volumen personalizado, integrado visualmente con KG TRACKER."""

    def __init__(
        self,
        parent,
        from_=0,
        to=100,
        length=120,
        command=None,
        bg="#1E1E2E",
        track_bg=COLOR_BORDER,
        fill_bg="#6C63FF",
        knob_bg="#F3F4F6",
        **kwargs
    ):
        super().__init__(parent, bg=bg, bd=0, highlightthickness=0, **kwargs)
        self._from = float(from_)
        self._to = float(to)
        self._value = self._from
        self._length = int(length)
        self._command = command
        self._bg = bg
        self._track_bg = track_bg
        self._fill_bg = fill_bg
        self._knob_bg = knob_bg
        self._dragging = False

        self._canvas = tk.Canvas(
            self,
            width=self._length,
            height=22,
            bg=bg,
            bd=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2"
        )
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", self._draw)
        self._canvas.bind("<Button-1>", self._click)
        self._canvas.bind("<B1-Motion>", self._drag)
        self._canvas.bind("<ButtonRelease-1>", self._release)

        self._draw()

    def _fraction(self):
        if self._to == self._from:
            return 0.0
        return max(0.0, min(1.0, (self._value - self._from) / (self._to - self._from)))

    def _value_from_x(self, x):
        width = max(1, self._canvas.winfo_width())
        margin = 7
        usable = max(1, width - (margin * 2))
        fraction = max(0.0, min(1.0, (x - margin) / usable))
        return self._from + fraction * (self._to - self._from)

    def _set_from_pointer(self, x):
        value = self._value_from_x(x)
        self.set(value)
        if self._command:
            self._command(value)

    def _click(self, event):
        self._dragging = True
        self._set_from_pointer(event.x)

    def _drag(self, event):
        if self._dragging:
            self._set_from_pointer(event.x)

    def _release(self, event):
        self._dragging = False

    def set(self, value):
        try:
            self._value = max(self._from, min(self._to, float(value)))
        except (TypeError, ValueError):
            return
        self._draw()

    def get(self):
        return self._value

    def set_colors(self, bg=None, track_bg=None, fill_bg=None, knob_bg=None):
        if bg is not None:
            self._bg = bg
        if track_bg is not None:
            self._track_bg = track_bg
        if fill_bg is not None:
            self._fill_bg = fill_bg
        if knob_bg is not None:
            self._knob_bg = knob_bg
        self.config(bg=self._bg)
        self._canvas.config(bg=self._bg)
        self._draw()

    def _draw(self, event=None):
        c = self._canvas
        c.delete("all")
        width = max(self._length, c.winfo_width())
        height = max(22, c.winfo_height())

        left = 7
        right = width - 7
        y = height / 2
        track_h = 5

        # Pista
        c.create_round_rect if False else None
        c.create_rectangle(
            left, y - track_h / 2, right, y + track_h / 2,
            fill=self._track_bg, outline=""
        )

        # Parte activa
        knob_x = left + (right - left) * self._fraction()
        c.create_rectangle(
            left, y - track_h / 2, knob_x, y + track_h / 2,
            fill=self._fill_bg, outline=""
        )

        # Tirador
        r = 7
        c.create_oval(
            knob_x - r, y - r, knob_x + r, y + r,
            fill=self._knob_bg, outline=self._fill_bg, width=2
        )

