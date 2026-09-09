from ui.widgets import RoundedButton, VolumeSlider
from ui.store_panel import StorePanel
"""Interfaz gráfica principal de K GAME TRACKER."""

# V5.0 - Control de volumen personalizado integrado en la interfaz

import os
import sys
import json
import re
import threading
import time
import queue
import webbrowser
import winreg
from datetime import datetime
import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pygame
import config

from config import (
    API_URL, API_HEADERS, EXCLUSIONES, STORES_MAPPING,
    COLOR_BG, COLOR_BG_CARD, COLOR_BG_DESC, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER, COLOR_WARNING, COLOR_ERROR,
    COLOR_SIDEBAR, COLOR_SIDEBAR_HOVER, COLOR_BORDER, COLOR_HOVER,
    WINDOW_TITLE, ICON_PATH, THUMBNAIL_SIZE,
    AUDIO_PATH, AUTOSTART_REG_PATH, AUTOSTART_APP_NAME,
    LOGO_PATH
)
from core.images import (
    descargar_imagen_thumbnail,
        limpiar_cache_imagenes,
    obtener_tamaño_cache
)


class VentanaPrincipal:
    """Ventana principal de K GAME TRACKER."""

    # ------------------------------------------------------------------------
    # INICIALIZACIÓN
    # ------------------------------------------------------------------------

    def __init__(self, parent=None, al_cerrar_app=None):
        self.parent = parent
        self.al_cerrar_app = al_cerrar_app
        self.ventana = tk.Toplevel(parent) if parent else tk.Tk()
        self.ventana.withdraw()
        self.ventana.title(WINDOW_TITLE)
        self.ventana.config(bg=COLOR_BG)
        self.ventana.minsize(980, 620)
        self.ventana.resizable(True, True)

        # Estado
        self.es_modo_oscuro = True
        self.audio_silenciado = False
        self.volumen_anterior = 20
        self.todas_activado = False
        self.juegos_cache_global = []
        self.active_filters = {store: False for store in STORES_MAPPING.values()}
        self.acordeon_estados = {}
        self.tienda_seleccionada = None
        self.bubble_widgets = {}
        self._icon_refs = []
        self._image_refs = []
        self.mostrando_reclamados = False
        self._status_anim_job = None
        self._status_anim_index = 0
        self._status_busqueda_inicio = 0.0
        self._busqueda_en_curso = False
        self.reclamados = self._cargar_reclamados()

        try:
            self.ventana.iconbitmap(ICON_PATH)
        except Exception:
            pass

        self._build_ui()
        # Audio gestionado por main.py durante el splash. No reinicializar aquí.
        self.ventana.geometry("1120x720")
        self._centrar()
        self.ventana.deiconify()
        self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar_ventana)

    # ------------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ------------------------------------------------------------------------

    def _build_ui(self):
        self.root_frame = tk.Frame(self.ventana, bg=COLOR_BG)
        self.root_frame.pack(fill="both", expand=True)

        # ------------------------------------------------------------
        # SIDEBAR
        # ------------------------------------------------------------
        self.sidebar = tk.Frame(self.root_frame, bg=COLOR_SIDEBAR, width=74)
        self.sidebar.pack(side="left", fill="y", expand=True)
        self.sidebar.pack_propagate(False)

        # Zona superior (logo, volver, TODAS/NINGUNA)
        self.sidebar_top = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR)
        self.sidebar_top.pack(side="top", fill="both", expand=True)

        # Logo
        try:
            logo_img = Image.open(LOGO_PATH).resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.logo_btn = tk.Label(self.sidebar_top, image=self.logo_photo, bg=COLOR_SIDEBAR, cursor="hand2")
            self.logo_btn.pack(pady=(16, 12))
            self.logo_btn.bind("<Button-1>", lambda e: self.resetear_app())
        except Exception:
            self.logo_btn = tk.Label(self.sidebar_top, text="K\nG", font=("Segoe UI", 17, "bold"),
                                     bg=COLOR_SIDEBAR, fg=COLOR_ACCENT_LIGHT, justify="center", cursor="hand2")
            self.logo_btn.pack(pady=(24, 28))
            self.logo_btn.bind("<Button-1>", lambda e: self.resetear_app())

        # Botón Volver
        self.btn_side_back = RoundedButton(
            self.sidebar_top,
            text="",
            command=self.volver_atras,
            width=54,
            height=50,
            bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT,
            fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER,
            radius=13,
            icon_path=self._icon_path("back.png"),
            icon_size=(28, 28)
        )
        self.btn_side_back.pack(pady=5)

        # Botón Todas / Ninguna (estilo principal)
        self.btn_side_todas = RoundedButton(
            self.sidebar_top,
            text="TODAS",
            command=self.toggle_todas,
            width=68,
            height=50,
            bg=COLOR_ACCENT,
            hover_bg=COLOR_ACCENT_HOVER,
            fg="white",
            border=COLOR_ACCENT,
            radius=13,
            icon_path=None,
            icon_size=(28, 28),
            font=("Segoe UI", 9, "bold")
        )
        self.btn_side_todas.pack_forget()  # oculto inicialmente

        # Zona inferior (ajustes y tema)
        self.sidebar_bottom = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR)
        self.sidebar_bottom.pack(side="bottom", fill="x", pady=(0, 10))

        # Botón Ko-fi (café) - Donaciones
        self.btn_side_kofi = RoundedButton(
            self.sidebar_bottom,
            text="",
            command=self.abrir_kofi,
            width=54,
            height=50,
            bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT,
            fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER,
            radius=13,
            icon_path=self._icon_path("cafe.png"),
            icon_size=(28, 28)
        )
        self.btn_side_kofi.pack(pady=5)
        
        self.btn_side_settings = RoundedButton(
            self.sidebar_bottom,
            text="",
            command=self.abrir_ajustes,
            width=54,
            height=50,
            bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT,
            fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER,
            radius=13,
            icon_path=self._icon_path("settings.png"),
            icon_size=(28, 28)
        )
        self.btn_side_settings.pack(pady=5)

        self.btn_side_theme = RoundedButton(
            self.sidebar_bottom,
            text="",
            command=self.alternar_tema,
            width=54,
            height=50,
            bg=COLOR_SIDEBAR,
            hover_bg=COLOR_ACCENT,
            fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER,
            radius=13,
            icon_path=self._icon_path("light_theme.png" if self.es_modo_oscuro else "dark_theme.png"),
            icon_size=(28, 28)
        )
        self.btn_side_theme.pack(pady=5)

        # ------------------------------------------------------------
        # CONTENIDO PRINCIPAL
        # ------------------------------------------------------------
        self.content = tk.Frame(self.root_frame, bg=COLOR_BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Panel de tiendas (altura suficiente)
        self.store_panel = tk.Frame(
            self.content,
            bg=COLOR_BG_CARD,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            height=220
        )
        self.store_panel.pack(fill="x", padx=28, pady=(16, 16))
        self.store_panel.pack_propagate(False)
        for i in range(9):
            self.store_panel.columnconfigure(i, weight=1)
        self._crear_burbujas_tiendas()

        # Botón buscar (SIN LUPA)
        action = tk.Frame(self.content, bg=COLOR_BG)
        action.pack(fill="x", padx=28, pady=(0, 12))
        action.columnconfigure(0, weight=1)
        self.btn_actualizar = RoundedButton(
            action,
            text="BUSCAR JUEGOS GRATUITOS",
            command=self.buscar_juegos,
            height=50,
            bg=COLOR_ACCENT,
            hover_bg=COLOR_ACCENT_HOVER,
            fg="white",
            border=COLOR_ACCENT,
            radius=14,
            font=("Segoe UI", 11, "bold"),
            icon_path=None,          # <-- LUPA ELIMINADA
            icon_size=(26, 26)       # <-- se mantiene pero no se usa
        )
        self.btn_actualizar.grid(row=0, column=0, sticky="ew")

        # Contenedor de resultados
        self.container = tk.Frame(self.content, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True, padx=28, pady=(0, 8))
        self.canvas = tk.Canvas(self.container, bg=COLOR_BG, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack_forget()
        self.frame_lista = tk.Frame(self.canvas, bg=COLOR_BG)
        self.frame_lista.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_lista, anchor="nw")
        self.canvas.bind("<Configure>", self._resize_canvas_content)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind_all("<MouseWheel>", self._mousewheel)

        # ------------------------------------------------------------
        # BARRA INFERIOR
        # ------------------------------------------------------------
        self.bottom = tk.Frame(self.content, bg=COLOR_BG)
        self.bottom.pack(fill="x", padx=28, pady=(0, 14))
        self.bottom.columnconfigure(0, weight=0)
        self.bottom.columnconfigure(1, weight=0)
        self.bottom.columnconfigure(2, weight=0)
        self.bottom.columnconfigure(3, weight=1)

        # Estado (izquierda): misma altura visual que RECLAMADOS.
        self.status_pill = tk.Frame(
            self.bottom,
            bg=COLOR_BG_CARD,
            width=142,
            height=34
        )
        self.status_pill.grid(row=0, column=0, sticky="w")
        self.status_pill.grid_propagate(False)

        self.status_label = tk.Label(
            self.status_pill,
            text="● LISTO",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_SUCCESS
        )
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        # Histórico de juegos reclamados
        self.btn_reclamados = RoundedButton(
            self.bottom,
            text="★ RECLAMADOS",
            command=self.mostrar_reclamados,
            width=142,
            height=34,
            bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER,
            fg=COLOR_ACCENT_LIGHT,
            border=COLOR_BORDER,
            radius=10,
            font=("Segoe UI", 8, "bold")
        )
        self.btn_reclamados.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # Dinero ahorrado por los juegos marcados como reclamados
        # Contador de ahorro: mismo "cuadro" visual que RECLAMADOS,
        # pero con texto dorado para darle sensación de recompensa.
        self.ahorro_pill = RoundedButton(
            self.bottom,
            text="$ AHORRADO : 0.00",
            command=lambda: None,
            width=156,
            height=34,
            bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER,
            fg=(COLOR_WARNING if config.CURRENT_THEME == "light" else "#F2C94C"),
            border=COLOR_BORDER,
            radius=10,
            font=("Segoe UI", 8, "bold")
        )
        self.ahorro_pill.grid(row=0, column=2, sticky="w", padx=(10, 0))
        self._actualizar_contador_ahorrado()

        # Volumen (derecha)
        right_frame = tk.Frame(self.bottom, bg=COLOR_BG)
        right_frame.grid(row=0, column=3, sticky="e")

        tk.Label(
            right_frame,
            text="VOLUMEN",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED
        ).pack(side="left", padx=(0, 8))

        self.slider_volumen = VolumeSlider(
            right_frame,
            from_=0,
            to=100,
            length=120,
            command=self.cambiar_volumen,
            bg=COLOR_BG,
            track_bg=COLOR_BORDER,
            fill_bg=COLOR_ACCENT,
            knob_bg=COLOR_TEXT_PRIMARY
        )
        self.slider_volumen.set(20)
        self.slider_volumen.pack(side="left", padx=(0, 8))

        self.btn_mute = RoundedButton(
            right_frame,
            text="",
            command=self.alternar_mute,
            width=42,
            height=38,
            bg=COLOR_BG_CARD,
            hover_bg=COLOR_HOVER,
            fg=COLOR_TEXT_PRIMARY,
            border=COLOR_BORDER,
            radius=11,
            icon_path=self._icon_path("volume.png"),
            icon_size=(21, 21)
        )
        self.btn_mute.pack(side="left", padx=(0, 6))

    # ------------------------------------------------------------------------
    # TIENDAS (estructura original con más altura)
    # ------------------------------------------------------------------------

    def _crear_burbujas_tiendas(self):
        tiendas = list(STORES_MAPPING.values())
        icon_map = {
            "Epic Games": "epic.png",
            "Steam": "steam.png",
            "GOG": "gog.png",
            "Amazon Prime": "amazon_prime.png",
            "Itch.io": "itch_io.png",
            "Humble Store": "humble_store.png",
            "Fanatical": "fanatical.png",
            "IndieGala": "indiegala.png",
            "Otras Plataformas": "other.png"
        }

        for idx, store in enumerate(tiendas):
            # Cada tienda es un Frame con altura suficiente
            item = tk.Frame(self.store_panel, bg=COLOR_BG_CARD, height=140, cursor="hand2")
            item.grid(row=0, column=idx, sticky="nsew", padx=6, pady=12)
            item.grid_propagate(False)

            canvas = tk.Canvas(item, width=80, height=80, bg=COLOR_BG_CARD,
                               highlightthickness=0, bd=0, cursor="hand2")
            canvas.pack(pady=(10, 4))

            # Icono
            icon_path = self._store_icon_path(icon_map.get(store, "other.png"))
            try:
                if os.path.exists(icon_path):
                    img = Image.open(icon_path).convert("RGBA")
                    img.thumbnail((64, 64), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self._icon_refs.append(photo)
                    canvas.create_image(40, 40, image=photo)
            except Exception:
                pass

            # Badge (contador)
            badge_bg = canvas.create_oval(62, 6, 78, 22, fill=COLOR_ERROR,
                                          outline=COLOR_BG_CARD, width=2, state="hidden")
            badge_text = canvas.create_text(70, 14, text="0", fill="white",
                                            font=("Segoe UI", 8, "bold"), state="hidden")

            label = tk.Label(item, text=store, font=("Segoe UI", 8, "bold"),
                             bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY, cursor="hand2")
            label.pack(pady=(0, 12))

            self.bubble_widgets[store] = {
                "canvas": canvas,
                "label": label,
                "badge_bg": badge_bg,
                "badge_text": badge_text,
                "item": item
            }

            for w in (item, canvas, label):
                w.bind("<Enter>", lambda e, s=store: self._on_bubble_hover(s, True))
                w.bind("<Leave>", lambda e, s=store: self._on_bubble_hover(s, False))
                w.bind("<Button-1>", lambda e, s=store: self._toggle_tienda(s))

    def _on_bubble_hover(self, store, is_hover):
        w = self.bubble_widgets[store]
        if is_hover:
            w["canvas"].config(bg=COLOR_ACCENT_LIGHT)
            w["label"].config(fg=COLOR_ACCENT_LIGHT)
        else:
            w["canvas"].config(bg=COLOR_BG_CARD)
            w["label"].config(fg=COLOR_SUCCESS if self.active_filters[store] else COLOR_TEXT_PRIMARY)

    # ------------------------------------------------------------------------
    # AUDIO
    # ------------------------------------------------------------------------

    def _inicializar_audio(self):
        try:
            if not os.path.exists(AUDIO_PATH):
                return
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.abspath(AUDIO_PATH))
            self.audio_silenciado = False
            self.volumen_anterior = 20
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(-1)
            self.slider_volumen.set(0)
            self._fade_audio(0)
        except Exception as e:
            print(f"⚠️ No se pudo inicializar el audio: {e}")

    def _fade_audio(self, porcentaje):
        try:
            porcentaje = max(0, min(20, porcentaje))
            pygame.mixer.music.set_volume(porcentaje / 100.0)
            self.slider_volumen.set(porcentaje)
            if porcentaje < 20:
                self.ventana.after(100, lambda: self._fade_audio(porcentaje + 1))
        except Exception:
            pass

    def cambiar_volumen(self, valor):
        try:
            if getattr(self, "btn_mute", None) is None:
                return
            porcentaje = max(0, min(100, int(float(valor))))
            pygame.mixer.music.set_volume(porcentaje / 100.0)
            if porcentaje > 0:
                self.audio_silenciado = False
                self.volumen_anterior = porcentaje
                self.btn_mute.set_icon(self._icon_path("volume.png"))
            else:
                self.audio_silenciado = True
                self.btn_mute.set_icon(self._icon_path("mute.png"))
        except Exception as e:
            print(f"⚠️ Error cambiando volumen: {e}")

    def alternar_mute(self):
        try:
            if not self.audio_silenciado:
                self.volumen_anterior = int(self.slider_volumen.get())
                pygame.mixer.music.set_volume(0.0)
                self.slider_volumen.set(0)
                self.audio_silenciado = True
                self.btn_mute.set_icon(self._icon_path("mute.png"))
            else:
                vol = self.volumen_anterior if self.volumen_anterior > 0 else 10
                pygame.mixer.music.set_volume(vol / 100.0)
                self.slider_volumen.set(vol)
                self.audio_silenciado = False
                self.btn_mute.set_icon(self._icon_path("volume.png"))
        except Exception as e:
            print(f"⚠️ Error alternando mute: {e}")

    def _detener_audio(self):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception:
            pass

    # ------------------------------------------------------------------------
    # DATOS Y API
    # ------------------------------------------------------------------------

    def _set_status(self, text, fg):
        if hasattr(self, "status_label") and self.status_label.winfo_exists():
            self.status_label.config(text=text, fg=fg)

    def _detener_animacion_estado(self):
        job = getattr(self, "_status_anim_job", None)
        if job is not None:
            try:
                self.ventana.after_cancel(job)
            except Exception:
                pass
        self._status_anim_job = None

    def _animar_estado_busqueda(self):
        if not getattr(self, "_busqueda_en_curso", False):
            self._detener_animacion_estado()
            return

        barras = ["▏▎▌▊▌▎▏", "▎▌▊▌▎▏▎", "▌▊▌▎▏▎▌", "▊▌▎▏▎▌▊",
                  "▌▎▏▎▌▊▌", "▎▏▎▌▊▌▎", "▏▎▌▊▌▎▏"]
        self.status_label.config(text=barras[self._status_anim_index % len(barras)], fg="#FF9F43")
        self._status_anim_index += 1
        self._status_anim_job = self.ventana.after(80, self._animar_estado_busqueda)

    def _iniciar_animacion_busqueda(self):
        self._detener_animacion_estado()
        self._busqueda_en_curso = True
        self._status_anim_index = 0
        self._status_busqueda_inicio = time.monotonic()
        self._animar_estado_busqueda()

    def _finalizar_busqueda(self, juegos_cache, conteos):
        # Garantiza que la animación haya durado aproximadamente 2 segundos.
        transcurrido = time.monotonic() - self._status_busqueda_inicio
        restante_ms = max(0, int(2000 - (transcurrido * 1000)))

        def aplicar():
            self._busqueda_en_curso = False
            self._detener_animacion_estado()
            self.juegos_cache_global = juegos_cache
            self.actualizar_insignias(conteos)
            self.btn_side_todas.pack()
            self.mostrando_reclamados = False
            self._actualizar_contador_ahorrado()
            self._actualizar_vista_juegos()
            self._set_status("● LISTO", COLOR_SUCCESS)

        self.ventana.after(restante_ms, aplicar)

    def _finalizar_error_busqueda(self, error):
        transcurrido = time.monotonic() - self._status_busqueda_inicio
        restante_ms = max(0, int(2000 - (transcurrido * 1000)))

        def aplicar():
            self._busqueda_en_curso = False
            self._detener_animacion_estado()
            self._set_status("● ERROR", COLOR_ERROR)
            messagebox.showerror("Error", f"No se pudieron cargar los juegos:\n{error}")

        self.ventana.after(restante_ms, aplicar)

    def buscar_juegos(self):
        if self._busqueda_en_curso:
            return

        self._iniciar_animacion_busqueda()
        resultado = queue.Queue(maxsize=1)

        def comprobar_resultado():
            try:
                tipo, datos = resultado.get_nowait()
            except queue.Empty:
                # Esta función se ejecuta siempre desde el hilo principal de Tk.
                if self._busqueda_en_curso:
                    self.ventana.after(25, comprobar_resultado)
                return

            if tipo == "ok":
                juegos_cache, conteos = datos
                self._finalizar_busqueda(juegos_cache, conteos)
            else:
                self._finalizar_error_busqueda(datos)

        def trabajador():
            try:
                limpiar_cache_imagenes()
                response = requests.get(API_URL, headers=API_HEADERS, timeout=10)
                response.raise_for_status()
                giveaways = response.json()
                if not isinstance(giveaways, list):
                    raise ValueError("Formato de API no válido")

                juegos_validos = []
                exclusiones_totales = list(EXCLUSIONES) + [
                    "dlc", "demo", "soundtrack", "ost", "expansion",
                    "pack", "bundle", "skin", "avatar"
                ]

                for g in giveaways:
                    titulo = str(g.get("title", "")).lower()
                    g_type = str(g.get("type", "")).lower()
                    if any(exc in g_type for exc in ["dlc", "loot", "demo", "soundtrack"]):
                        continue
                    if any(exc in titulo for exc in exclusiones_totales):
                        continue
                    juegos_validos.append(g)

                juegos_unicos = {}
                for juego in juegos_validos:
                    clave = self._clave_juego(juego)
                    if clave not in juegos_unicos:
                        juegos_unicos[clave] = juego

                juegos_cache = list(juegos_unicos.values())

                historico_actualizado = False
                for juego in juegos_cache:
                    clave = self._clave_juego(juego)
                    registro = self.reclamados.get(clave)
                    if registro is not None:
                        valor_actual = self._valor_juego(juego)
                        if valor_actual > 0 and self._parsear_valor_juego(
                            registro.get("worth_value")
                        ) <= 0:
                            registro["worth_value"] = valor_actual
                            registro["worth"] = str(juego.get("worth") or "")
                            historico_actualizado = True

                if historico_actualizado:
                    self._guardar_reclamados()

                disponibles = [
                    j for j in juegos_cache if not self._esta_reclamado(j)
                ]
                conteos = {s: 0 for s in STORES_MAPPING.values()}
                for juego in disponibles:
                    tienda = self._asignar_tienda(juego)
                    if tienda in conteos:
                        conteos[tienda] += 1

                # El hilo de trabajo NO toca Tkinter. Solo entrega el resultado.
                resultado.put(("ok", (juegos_cache, conteos)))

            except Exception as e:
                # El hilo de trabajo NO llama a self.ventana.after().
                resultado.put(("error", e))

        # El polling se registra desde el hilo principal antes de lanzar el worker.
        self.ventana.after(25, comprobar_resultado)
        threading.Thread(target=trabajador, daemon=True).start()


    def _asignar_tienda(self, juego):
        platforms = str(juego.get("platforms", "")).lower()
        store_field = str(juego.get("store", "")).lower()
        title = str(juego.get("title", "")).lower()
        url = str(juego.get("open_giveaway_url", "")).lower()
        t = f"{platforms} {store_field} {title} {url}"

        if any(k in t for k in ["prime gaming", "amazon", "twitch", "luna"]):
            return "Amazon Prime"
        if any(k in t for k in ["gog", "gog.com"]):
            return "GOG"
        if any(k in t for k in ["humble", "humblebundle"]):
            return "Humble Store"
        if any(k in t for k in ["fanatical", "bundlestars"]):
            return "Fanatical"
        if any(k in t for k in ["epic", "epicgames"]):
            return "Epic Games"
        if "steam" in t:
            return "Steam"
        if any(k in t for k in ["itch", "itch.io"]):
            return "Itch.io"
        if "indiegala" in t:
            return "IndieGala"
        return "Otras Plataformas"

    def actualizar_insignias(self, conteos):
        for store, count in conteos.items():
            if store not in self.bubble_widgets:
                continue
            w = self.bubble_widgets[store]
            state = "normal" if count > 0 else "hidden"
            w["canvas"].itemconfig(w["badge_bg"], state=state)
            w["canvas"].itemconfig(w["badge_text"], state=state, text=str(count))

    # ------------------------------------------------------------------------
    # VISTA DE JUEGOS
    # ------------------------------------------------------------------------

    def _actualizar_vista_juegos(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        self._image_refs = []

        if self.mostrando_reclamados:
            self._mostrar_lista_reclamados()
            return

        tiendas = [s for s, a in self.active_filters.items() if a]
        if not tiendas:
            self.scrollbar.pack_forget()
            return
        self.scrollbar.pack(side="right", fill="y")

        for store in tiendas:
            juegos = [
                j for j in self.juegos_cache_global
                if self._asignar_tienda(j) == store and not self._esta_reclamado(j)
            ]
            open_ = self.acordeon_estados.get(store, True)

            header = tk.Frame(self.frame_lista, bg=COLOR_BG_CARD)
            header.pack(fill="x", pady=(8, 4))
            header.bind("<Button-1>", lambda e, s=store: self._toggle_acordeon(s))

            arrow = "▼" if open_ else "▶"
            lbl = tk.Label(header, text=f"{arrow}   {store.upper()}", font=("Segoe UI", 10, "bold"),
                           bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY, padx=14, pady=10, cursor="hand2")
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda e, s=store: self._toggle_acordeon(s))

            tk.Label(header, text=f"{len(juegos)} ofertas", font=("Segoe UI", 8, "bold"),
                     bg=COLOR_BG_CARD, fg=COLOR_ACCENT_LIGHT, padx=14).pack(side="right")

            if not open_:
                continue
            if not juegos:
                tk.Label(self.frame_lista, text=f"No hay elementos disponibles en {store} actualmente.",
                         font=("Segoe UI", 9, "italic"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=6)
                continue
            for juego in juegos:
                self._crear_tarjeta_juego(juego, store)

    def _toggle_acordeon(self, store):
        self.acordeon_estados[store] = not self.acordeon_estados.get(store, True)
        self._actualizar_vista_juegos()

    def _crear_tarjeta_juego(self, juego, nombre_tienda):
        titulo = juego.get("title", "Elemento sin título")
        thumb_url = juego.get("image") or juego.get("thumbnail")
        link_url = str(juego.get("open_giveaway_url") or "").strip()
        descripcion = " ".join(str(juego.get("description", "Sin descripción disponible.")).split())
        if len(descripcion) > 170:
            descripcion = descripcion[:167] + "..."

        card = tk.Frame(self.frame_lista, bg=COLOR_BG_CARD, highlightthickness=1, highlightbackground=COLOR_BORDER)
        card.pack(fill="x", pady=4)
        card.columnconfigure(1, weight=1)

        image_box = tk.Frame(card, bg=COLOR_BG_DESC, width=190, height=104)
        image_box.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsw")
        image_box.grid_propagate(False)

        photo = descargar_imagen_thumbnail(thumb_url)
        if photo:
            self._image_refs.append(photo)
            tk.Label(image_box, image=photo, bg=COLOR_BG_DESC).place(relx=0.5, rely=0.5, anchor="center")
        else:
            tk.Label(image_box, text="SIN\nMINIATURA", font=("Segoe UI", 8, "bold"),
                     bg=COLOR_BG_DESC, fg=COLOR_TEXT_MUTED).place(relx=0.5, rely=0.5, anchor="center")

        info = tk.Frame(card, bg=COLOR_BG_CARD)
        info.grid(row=0, column=1, sticky="nsew", padx=(4, 10), pady=(11, 4))
        tk.Label(info, text=titulo, font=("Segoe UI", 11, "bold"), bg=COLOR_BG_CARD,
                 fg=COLOR_TEXT_PRIMARY, anchor="w", justify="left", wraplength=600).pack(fill="x")
        tk.Label(info, text=descripcion, font=("Segoe UI", 8), bg=COLOR_BG_CARD,
                 fg=COLOR_TEXT_SECONDARY, anchor="w", justify="left", wraplength=600).pack(fill="x", pady=(4, 0))
        tk.Label(info, text=nombre_tienda.upper(), font=("Segoe UI", 7, "bold"),
                 bg=COLOR_BG_CARD, fg=COLOR_ACCENT_LIGHT, anchor="w").pack(fill="x", pady=(6, 0))

        valor_juego = self._valor_juego(juego)
        if valor_juego > 0:
            tk.Label(
                info,
                text=f"VALOR ESTIMADO: ${valor_juego:,.2f}",
                font=("Segoe UI", 7, "bold"),
                bg=COLOR_BG_CARD,
                fg=COLOR_SUCCESS,
                anchor="w"
            ).pack(fill="x", pady=(3, 0))

        esta_reclamado = self._esta_reclamado(juego)

        # Los dos botones tienen funciones independientes:
        # RECLAMAR abre la oferta; MARCAR RECLAMADO la guarda en el histórico.
        action_frame = tk.Frame(card, bg=COLOR_BG_CARD)
        action_frame.grid(row=0, column=2, rowspan=2, padx=(2, 12), pady=10, sticky="e")

        if esta_reclamado:
            btn = RoundedButton(
                action_frame,
                text="✓ RECLAMADO",
                command=lambda j=juego: self._alternar_reclamado(j),
                width=128,
                height=38,
                bg=COLOR_ACCENT,
                hover_bg=COLOR_ACCENT_HOVER,
                fg="white",
                border=COLOR_ACCENT,
                radius=11,
                font=("Segoe UI", 8, "bold")
            )
            btn.pack()
        else:
            btn_reclamar = RoundedButton(
                action_frame,
                text="RECLAMAR",
                command=lambda u=link_url: self._abrir_reclamacion(u),
                width=128,
                height=36,
                bg=COLOR_SUCCESS,
                hover_bg=COLOR_SUCCESS_HOVER,
                fg="white",
                border=COLOR_SUCCESS,
                radius=11,
                font=("Segoe UI", 8, "bold"),
                icon_path=self._action_icon_path("open_link.png"),
                icon_size=(18, 18)
            )
            btn_reclamar.pack(pady=(0, 5))

            btn_marcar = RoundedButton(
                action_frame,
                text="★ RECLAMADO",
                command=lambda j=juego: self._alternar_reclamado(j),
                width=128,
                height=32,
                bg=COLOR_BG_CARD,
                hover_bg=COLOR_HOVER,
                fg=COLOR_ACCENT_LIGHT,
                border=COLOR_BORDER,
                radius=10,
                font=("Segoe UI", 7, "bold")
            )
            btn_marcar.pack()

    # ------------------------------------------------------------------------
    # HISTÓRICO DE RECLAMADOS
    # ------------------------------------------------------------------------

    def _ruta_reclamados(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "reclamados.json")

    def _cargar_reclamados(self):
        ruta = self._ruta_reclamados()
        try:
            if not os.path.exists(ruta):
                return {}

            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)

            if not isinstance(datos, dict):
                return {}

            # Migración/limpieza: versiones anteriores podían guardar el mismo
            # juego varias veces con claves URL/ID diferentes. Recalculamos la
            # clave estable juego+tienda y conservamos solo el registro más
            # reciente de cada juego.
            limpios = {}
            for registro in datos.values():
                if not isinstance(registro, dict):
                    continue

                titulo = " ".join(str(registro.get("title") or "").lower().split()).strip()
                tienda = " ".join(str(registro.get("store") or "Otras Plataformas").lower().split()).strip()

                for sufijo in (" giveaway", " - giveaway"):
                    if titulo.endswith(sufijo):
                        titulo = titulo[:-len(sufijo)].strip()

                clave = f"game:{tienda}|{titulo}"

                if clave not in limpios:
                    registro_limpio = dict(registro)
                    if "worth_value" not in registro_limpio:
                        registro_limpio["worth_value"] = self._parsear_valor_juego(registro_limpio.get("worth"))
                    registro_limpio["key"] = clave
                    limpios[clave] = registro_limpio
                else:
                    # Si hay duplicados, conservamos el que tenga fecha más reciente.
                    anterior = limpios[clave]
                    if str(registro.get("claimed_at", "")) > str(anterior.get("claimed_at", "")):
                        registro_limpio = dict(registro)
                        if "worth_value" not in registro_limpio:
                            registro_limpio["worth_value"] = self._parsear_valor_juego(registro_limpio.get("worth"))
                        registro_limpio["key"] = clave
                        limpios[clave] = registro_limpio

            # Guardar la migración solo si realmente había claves antiguas/duplicadas.
            if limpios != datos:
                try:
                    with open(ruta, "w", encoding="utf-8") as f:
                        json.dump(limpios, f, ensure_ascii=False, indent=2)
                except Exception:
                    pass

            return limpios

        except Exception:
            return {}

    def _parsear_valor_juego(self, valor):
        """Convierte el campo `worth` de GamerPower a USD numérico."""
        if valor is None:
            return 0.0
        if isinstance(valor, (int, float)):
            return max(0.0, float(valor))

        texto = str(valor).strip()
        if not texto or texto.upper() in {"N/A", "NA", "NONE", "NULL", "FREE"}:
            return 0.0

        # GamerPower suele devolver valores como "$19.99".
        limpio = re.sub(r"[^0-9,.-]", "", texto)
        if not limpio:
            return 0.0

        # Admite tanto 19.99 como 19,99 y separadores de miles.
        if "," in limpio and "." in limpio:
            if limpio.rfind(",") > limpio.rfind("."):
                limpio = limpio.replace(".", "").replace(",", ".")
            else:
                limpio = limpio.replace(",", "")
        elif "," in limpio:
            partes = limpio.split(",")
            if len(partes[-1]) in (1, 2):
                limpio = "".join(partes[:-1]) + "." + partes[-1]
            else:
                limpio = limpio.replace(",", "")

        try:
            return max(0.0, float(limpio))
        except (TypeError, ValueError):
            return 0.0

    def _valor_juego(self, juego):
        """Devuelve el valor estimado del juego en USD."""
        if not isinstance(juego, dict):
            return 0.0
        return self._parsear_valor_juego(juego.get("worth_value", juego.get("worth")))

    def _dinero_ahorrado(self):
        """Suma el valor de todos los juegos actualmente reclamados."""
        total = 0.0
        for registro in self.reclamados.values():
            if isinstance(registro, dict):
                total += self._parsear_valor_juego(
                    registro.get("worth_value", registro.get("worth"))
                )
        return total

    def _actualizar_contador_ahorrado(self):
        """Actualiza el contador visual de ahorro sin romper la UI si aún no existe."""
        if not hasattr(self, "ahorro_pill"):
            return
        total = self._dinero_ahorrado()
        color_ahorro = COLOR_WARNING if config.CURRENT_THEME == "light" else "#F2C94C"
        self.ahorro_pill.config(text=f"$ AHORRADO : {total:,.2f}", fg=color_ahorro)

    def _guardar_reclamados(self):
        try:
            ruta = self._ruta_reclamados()
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(self.reclamados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showwarning(
                "Aviso",
                f"No se pudo guardar el histórico de reclamados:\n{e}"
            )

    def _clave_juego(self, juego):
        """
        Identidad funcional del juego para KG TRACKER.

        No usamos la URL ni el ID como clave principal porque una misma
        oferta puede aparecer con URLs/IDs diferentes. Para el histórico
        interesa saber si el usuario ya reclamó ESE JUEGO EN ESA TIENDA.
        """
        titulo = " ".join(str(juego.get("title") or "").lower().split()).strip()
        tienda = " ".join(str(self._asignar_tienda(juego) or "").lower().split()).strip()

        # Limpiar etiquetas habituales del título que pueden variar entre
        # respuestas de la API sin cambiar realmente el juego.
        for sufijo in (" giveaway", " - giveaway"):
            if titulo.endswith(sufijo):
                titulo = titulo[:-len(sufijo)].strip()

        return f"game:{tienda}|{titulo}"

    def _esta_reclamado(self, juego):
        clave_guardada = juego.get("__reclamado_key")
        if clave_guardada:
            return clave_guardada in self.reclamados
        return self._clave_juego(juego) in self.reclamados

    def _abrir_reclamacion(self, url):
        """Abre la página del giveaway sin marcarlo como reclamado."""
        if url:
            webbrowser.open(url)

    def _alternar_reclamado(self, juego):
        clave = self._clave_juego(juego)
        if clave in self.reclamados:
            del self.reclamados[clave]
        else:
            self.reclamados[clave] = {
                "key": clave,
                "id": juego.get("id"),
                "title": str(juego.get("title") or "Elemento sin título"),
                "store": self._asignar_tienda(juego),
                "image": juego.get("image") or juego.get("thumbnail"),
                "description": juego.get("description") or "",
                "open_giveaway_url": str(juego.get("open_giveaway_url") or ""),
                "worth": str(juego.get("worth") or ""),
                "worth_value": self._valor_juego(juego),
                "worth_currency": "USD",
                "claimed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        self._guardar_reclamados()
        self._actualizar_contador_ahorrado()
        self._actualizar_vista_juegos()

        disponibles = [
            j for j in self.juegos_cache_global
            if not self._esta_reclamado(j)
        ]
        conteos = {s: 0 for s in STORES_MAPPING.values()}
        for j in disponibles:
            tienda = self._asignar_tienda(j)
            if tienda in conteos:
                conteos[tienda] += 1
        self.actualizar_insignias(conteos)
        if self.mostrando_reclamados:
            self._set_status("● LISTO", COLOR_SUCCESS)
        else:
            self._set_status("● LISTO", COLOR_SUCCESS)

    def mostrar_reclamados(self):
        self.mostrando_reclamados = not self.mostrando_reclamados

        if self.mostrando_reclamados:
            self.btn_reclamados.config(
                text="★ VER RECLAMADOS",
                bg=COLOR_ACCENT,
                activebackground=COLOR_ACCENT_HOVER,
                fg="white"
            )
            self._set_status("● LISTO", COLOR_SUCCESS)
        else:
            self.btn_reclamados.config(
                text="★ RECLAMADOS",
                bg=COLOR_BG_CARD,
                activebackground=COLOR_SIDEBAR_HOVER,
                fg=COLOR_ACCENT_LIGHT
            )
            disponibles = [
                j for j in self.juegos_cache_global
                if not self._esta_reclamado(j)
            ]
            self._set_status("● LISTO", COLOR_SUCCESS)

        self._actualizar_vista_juegos()

    def _mostrar_lista_reclamados(self):
        self.scrollbar.pack(side="right", fill="y")

        if not self.reclamados:
            tk.Label(
                self.frame_lista,
                text="AÚN NO TIENES JUEGOS RECLAMADOS",
                font=("Segoe UI", 11, "bold"),
                bg=COLOR_BG,
                fg=COLOR_TEXT_MUTED
            ).pack(pady=40)
            return

        header = tk.Frame(self.frame_lista, bg=COLOR_BG_CARD)
        header.pack(fill="x", pady=(8, 8))
        tk.Label(
            header,
            text=f"★  MIS RECLAMADOS  ·  {len(self.reclamados)}",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT_PRIMARY,
            padx=14,
            pady=10
        ).pack(side="left")

        for registro in sorted(
            self.reclamados.values(),
            key=lambda x: str(x.get("claimed_at", "")),
            reverse=True
        ):
            juego = {
                "id": registro.get("id"),
                "title": registro.get("title", "Elemento sin título"),
                "store": registro.get("store", ""),
                "image": registro.get("image"),
                "thumbnail": registro.get("image"),
                "description": registro.get("description", ""),
                "open_giveaway_url": registro.get("open_giveaway_url", ""),
                "worth": registro.get("worth", ""),
                "worth_value": registro.get("worth_value", 0),
                "__reclamado_key": registro.get("key")
            }
            self._crear_tarjeta_juego(juego, registro.get("store", "Otras Plataformas"))

    def abrir_enlace(self, url):
        if url:
            webbrowser.open(url)

    # ------------------------------------------------------------------------
    # INTERACCIÓN
    # ------------------------------------------------------------------------

    def toggle_todas(self):
        if self.todas_activado:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.todas_activado = False
            self.btn_side_todas.config(text="TODAS")
        else:
            for s in self.active_filters:
                self.active_filters[s] = True
                self.acordeon_estados[s] = True
            self.todas_activado = True
            self.btn_side_todas.config(text="NINGUNA")

        for s, w in self.bubble_widgets.items():
            active = self.active_filters[s]
            w["label"].config(fg=COLOR_SUCCESS if active else COLOR_TEXT_PRIMARY)
        self._actualizar_vista_juegos()

    def _toggle_tienda(self, store):
        if self.todas_activado:
            self.todas_activado = False
            self.btn_side_todas.config(text="TODAS")

        if self.active_filters[store]:
            self.active_filters[store] = False
            if store in self.acordeon_estados:
                self.acordeon_estados[store] = False
        else:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.active_filters[store] = True
            self.acordeon_estados[store] = True

        for s, w in self.bubble_widgets.items():
            active = self.active_filters[s]
            w["label"].config(fg=COLOR_SUCCESS if active else COLOR_TEXT_PRIMARY)
        self._actualizar_vista_juegos()

    # ------------------------------------------------------------------------
    # NAVEGACIÓN
    # ------------------------------------------------------------------------

    def volver_atras(self):
        self.mostrando_reclamados = False
        self.btn_reclamados.config(
            text="★ RECLAMADOS",
            bg=COLOR_BG_CARD,
            activebackground=COLOR_SIDEBAR_HOVER,
            fg=COLOR_ACCENT_LIGHT
        )
        for s in self.active_filters:
            self.active_filters[s] = False
        self.tienda_seleccionada = None
        self.todas_activado = False
        self.btn_side_todas.config(text="TODAS")
        self.btn_side_todas.pack_forget()

        for s, w in self.bubble_widgets.items():
            w["label"].config(fg=COLOR_TEXT_PRIMARY)

        self.juegos_cache_global = []
        self._actualizar_vista_juegos()
        self._set_status("● LISTO", COLOR_SUCCESS)

    def resetear_app(self):
        self.volver_atras()
        self.ventana.update_idletasks()

    # ------------------------------------------------------------------------
    # TEMA
    # ------------------------------------------------------------------------

    def alternar_tema(self):
        """Cambia entre tema oscuro y claro reconstruyendo la UI con la nueva paleta."""
        busqueda_activa = getattr(self, "_busqueda_en_curso", False)

        # Detener cualquier after de la animación antes de destruir los widgets.
        self._detener_animacion_estado()

        estado = {
            "active_filters": dict(getattr(self, "active_filters", {})),
            "acordeon_estados": dict(getattr(self, "acordeon_estados", {})),
            "tienda_seleccionada": getattr(self, "tienda_seleccionada", None),
            "mostrando_reclamados": getattr(self, "mostrando_reclamados", False),
            "todas_activado": getattr(self, "todas_activado", False),
            "juegos_cache_global": list(getattr(self, "juegos_cache_global", [])),
            "volumen": getattr(self, "volumen", 0.1),
            "silenciado": getattr(self, "silenciado", False),
        }

        config.CURRENT_THEME = "light" if config.CURRENT_THEME == "dark" else "dark"
        tema = config.THEMES[config.CURRENT_THEME]

        for nombre, valor in tema.items():
            globals()[nombre] = valor
            setattr(config, nombre, valor)

        icon_path = self._icon_path(
            "dark_theme.png" if config.CURRENT_THEME == "dark" else "light_theme.png"
        )

        self.es_modo_oscuro = config.CURRENT_THEME == "dark"

        # Reconstruimos para que todos los widgets nazcan con la paleta correcta.
        self.root_frame.destroy()
        self._build_ui()

        self.active_filters = estado["active_filters"]

        # Si la búsqueda sigue activa, continuar la animación en el nuevo widget.
        if busqueda_activa:
            self._busqueda_en_curso = True
            self._status_busqueda_inicio = getattr(
                self, "_status_busqueda_inicio", time.monotonic()
            )
            self._animar_estado_busqueda()
        self.acordeon_estados = estado["acordeon_estados"]
        self.tienda_seleccionada = estado["tienda_seleccionada"]
        self.mostrando_reclamados = estado["mostrando_reclamados"]
        self.todas_activado = estado["todas_activado"]
        self.juegos_cache_global = estado["juegos_cache_global"]
        self.volumen = estado["volumen"]
        self.silenciado = estado["silenciado"]

        if hasattr(self, "btn_side_theme"):
            self.btn_side_theme.set_icon(icon_path)

        self._actualizar_vista_juegos()

    def _apply_theme(self, bg, card, desc, text, secondary, icon_path):
        """Compatibilidad con llamadas antiguas; aplica el tema mediante reconstrucción."""
        self.alternar_tema()

    # ------------------------------------------------------------------------
    # AJUSTES
    # ------------------------------------------------------------------------

    def abrir_ajustes(self):
        """Abre la ventana modal de ajustes de configuración."""
        modal = tk.Toplevel(self.ventana)
        modal.withdraw()
        modal.title("Ajustes de Configuración")
        modal.geometry("600x500")
        modal.configure(bg="#121218")
        modal.resizable(False, False)
        modal.transient(self.ventana)
        modal.grab_set()

        try:
            modal.iconbitmap(ICON_PATH)
        except Exception:
            pass

        modal.update_idletasks()
        x = self.ventana.winfo_x() + (self.ventana.winfo_width() - 600) // 2
        y = self.ventana.winfo_y() + (self.ventana.winfo_height() - 500) // 2
        modal.geometry(f"+{x}+{y}")

        # Contenedor principal
        main_frame = tk.Frame(modal, bg="#1a1a24")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Header
        header_frame = tk.Frame(main_frame, bg="#1a1a24")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title_label = tk.Label(
            header_frame, 
            text="AJUSTES DE CONFIGURACIÓN", 
            font=("Segoe UI", 12, "bold"), 
            bg="#1a1a24", 
            fg="white"
        )
        title_label.pack(side="left")

        btn_close = tk.Button(
            header_frame, 
            text="✕", 
            width=3, 
            bg="#1a1a24", 
            fg="white", 
            relief="flat",
            activebackground="#2a2a3a",
            activeforeground="white",
            command=modal.destroy
        )
        btn_close.pack(side="right")

        # Separador
        sep = tk.Frame(main_frame, height=2, bg="#2a2a3a")
        sep.pack(fill="x", padx=20, pady=10)

        # Opciones
        options_frame = tk.Frame(main_frame, bg="#1a1a24")
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)

        def crear_fila(texto, valores):
            row = tk.Frame(options_frame, bg="#1a1a24")
            row.pack(fill="x", pady=12)
            lbl = tk.Label(row, text=texto, bg="#1a1a24", fg="white", font=("Segoe UI", 11))
            lbl.pack(side="left")
            
            # Usamos un Combobox o OptionMenu nativo estilizado
            var = tk.StringVar(value=valores[0])
            menu = tk.OptionMenu(row, var, *valores)
            menu.config(bg="#121218", fg="white", activebackground="#2a2a3a", activeforeground="white", highlightthickness=0, relief="flat", width=15)
            menu["menu"].config(bg="#121218", fg="white")
            menu.pack(side="right")
            return var

        crear_fila("Idioma de la interfaz", ["Español (ES)", "English (EN)"])
        crear_fila("Tema visual", ["Neón Cyberpunk", "Oscuro Clásico", "Minimalista"])
        crear_fila("Buscar ofertas automáticamente", ["Al iniciar", "Cada hora", "Desactivado"])

        # Checkbox iniciar minimizado
        chk_frame = tk.Frame(options_frame, bg="#1a1a24")
        chk_frame.pack(fill="x", pady=12)
        lbl_chk = tk.Label(chk_frame, text="Iniciar minimizado con Windows", bg="#1a1a24", fg="white", font=("Segoe UI", 11))
        lbl_chk.pack(side="left")
        
        chk_var = tk.IntVar()
        chk = tk.Checkbutton(chk_frame, variable=chk_var, bg="#1a1a24", activebackground="#1a1a24", selectcolor="#121218")
        chk.pack(side="right")

        # Botón guardar
        btn_guardar = tk.Button(
            main_frame, 
            text="GUARDAR CAMBIOS", 
            height=2,
            bg="#5865F2", 
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=modal.destroy
        )
        btn_guardar.pack(fill="x", padx=20, pady=(10, 20))

        modal.deiconify()
    def _comprobar_autostart(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, AUTOSTART_APP_NAME)
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def _guardar_autostart(self, habilitar):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH, 0, winreg.KEY_ALL_ACCESS)
            if habilitar:
                script_path = os.path.abspath(sys.argv[0])
                cmd = f'"{sys.executable}" "{script_path}"'
                winreg.SetValueEx(key, AUTOSTART_APP_NAME, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, AUTOSTART_APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            messagebox.showwarning("Aviso", f"No se pudo modificar el inicio automático:\n{e}")

    # ------------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------------

    

    def _centrar(self):
        self.ventana.update_idletasks()
        w, h = self.ventana.winfo_width(), self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() - w) // 2
        y = (self.ventana.winfo_screenheight() - h) // 2
        self.ventana.geometry(f"{w}x{h}+{x}+{y}")

    def _resize_canvas_content(self, event):
        self.canvas.itemconfigure(self.canvas_window, width=max(1, event.width))

    def _mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    # ------------------------------------------------------------------------
    # CIERRE
    # ------------------------------------------------------------------------

    def _cerrar_ventana(self):
        self._detener_audio()
        limpiar_cache_imagenes()
        self.ventana.destroy()

    def mostrar(self):
        self.ventana.deiconify()
        self._centrar()

    def run(self):
        self.ventana.wait_window()

    # ------------------------------------------------------------------------
    # RUTAS DE ASSETS
    # ------------------------------------------------------------------------

    def _icons_root(self):
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "icons"
        )

    def _icon_path(self, filename):
        return os.path.join(self._icons_root(), "navigation_ui", filename)

    def _action_icon_path(self, filename):
        return os.path.join(self._icons_root(), "actions", filename)

    def _store_icon_path(self, filename):
        return os.path.join(self._icons_root(), "stores", filename)


    def abrir_kofi(self):
        """Abre la ventana modal independiente de Ko-fi."""
        from ui.kofi_modal import KofiModal
        KofiModal(self.ventana)

