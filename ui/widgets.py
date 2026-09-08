"""Widgets reutilizables para la interfaz gráfica.

Nota: Este módulo contiene componentes que pueden usarse
en futuras versiones. Actualmente, la lógica está en main_window.py
"""

import webbrowser
import tkinter as tk
from tkinter import ttk

from config import (
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
