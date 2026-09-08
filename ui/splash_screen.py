"""Pantalla de bienvenida con transparencia real, sombra y animación.

- Si el logo tiene canal alfa, se usa directamente.
- En Windows se aplica chroma key con un color seguro (#010101) para que
  el sistema recorte el rectángulo de fondo y solo quede la silueta.
- En otros sistemas (macOS/Linux) se usa COLOR_BG como fallback.
- Incluye animación de entrada (fade + zoom) y salida (fade).
"""

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from config import COLOR_BG, LOGO_PATH, SPLASH_MAX_WIDTH, SPLASH_CORNER_RADIUS

# ---- Parámetros de animación ----
DURACION_ENTRADA_MS = 380
DURACION_ESPERA_MS = 900
DURACION_SALIDA_MS = 280
INTERVALO_FRAME_MS = 16
ESCALA_INICIAL = 0.82

# ---- Parámetros de la sombra ----
SOMBRA_MARGEN = 26
SOMBRA_DESPLAZAMIENTO_Y = 8
SOMBRA_DIFUMINADO = 10
SOMBRA_OPACIDAD = 95
SOMBRA_UMBRAL_CORTE = 18

# Color que se usará como clave de transparencia (debe ser un color que
# NO aparezca en el logo). #010101 es negro muy oscuro, raramente usado.
CHROMA_KEY = "#010101"

def _color_rgba(hex_color):
    """Convierte #RRGGBB a (r, g, b, 255)."""
    hex_color = hex_color.lstrip("#")
    return (int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
            255)

def _crear_sombra(tam_logo, radio):
    """Genera una máscara de sombra difuminada para el logo."""
    ancho, alto = tam_logo
    # Lienzo más grande para la sombra
    lienzo = Image.new("L", (ancho + SOMBRA_MARGEN*2,
                             alto + SOMBRA_MARGEN*2), 0)
    draw = ImageDraw.Draw(lienzo)
    draw.rounded_rectangle(
        [
            (SOMBRA_MARGEN, SOMBRA_MARGEN + SOMBRA_DESPLAZAMIENTO_Y),
            (SOMBRA_MARGEN + ancho - 1,
             SOMBRA_MARGEN + alto - 1 + SOMBRA_DESPLAZAMIENTO_Y)
        ],
        radius=radio,
        fill=SOMBRA_OPACIDAD
    )
    # Desenfoque gaussiano
    lienzo = lienzo.filter(ImageFilter.GaussianBlur(SOMBRA_DIFUMINADO))
    # Recortar valores muy bajos para evitar un halo enorme
    arr = np.asarray(lienzo).astype(np.float32)
    arr = np.where(arr < SOMBRA_UMBRAL_CORTE, 0, arr)
    rango = 255.0 - SOMBRA_UMBRAL_CORTE
    arr = np.where(arr > 0, (arr - SOMBRA_UMBRAL_CORTE) / rango * 255.0, 0)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="L")

def _ease_out_cubic(t):
    """Curva de aceleración suave (ease-out)."""
    t = max(0.0, min(1.0, t))
    return 1 - pow(1 - t, 3)

def mostrar_splash_inicio(root, al_terminar):
    """
    Muestra el splash con el logo transparente, sombra y animación.
    Al terminar, destruye la ventana y llama a al_terminar().
    """
    # ---- Crear ventana splash ----
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.withdraw()  # oculta hasta tener el primer frame
    try:
        splash.attributes("-topmost", True)
    except tk.TclError:
        pass

    # ---- Cargar y preparar el logo ----
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
    except Exception as e:
        # Si falla, mostrar texto de emergencia
        splash.geometry("300x150")
        splash.configure(bg=COLOR_BG)
        tk.Label(splash, text="K GAME TRACKER",
                 font=("Segoe UI", 24, "bold"),
                 bg=COLOR_BG, fg="white").pack(expand=True)
        splash.deiconify()
        splash.after(1200, lambda: (splash.destroy(), al_terminar()))
        print(f"⚠️ Splash: no se pudo cargar el logo: {e}")
        return

    # Redimensionar si supera el máximo
    if logo.width > SPLASH_MAX_WIDTH:
        ratio = SPLASH_MAX_WIDTH / float(logo.width)
        logo = logo.resize((SPLASH_MAX_WIDTH,
                            max(1, int(logo.height * ratio))),
                           Image.Resampling.LANCZOS)

    # Asegurar que tiene canal alfa
    if logo.mode != "RGBA":
        logo = logo.convert("RGBA")

    # Obtener tamaño original del logo (sin sombra)
    tam_logo = logo.size

    # ---- Configurar transparencia (chroma key) ----
    transparencia_activa = False
    try:
        # Establecer el color clave en la ventana
        splash.configure(bg=CHROMA_KEY)
        splash.attributes("-transparentcolor", CHROMA_KEY)
        transparencia_activa = True
    except tk.TclError:
        # Fallback a fondo sólido con COLOR_BG
        splash.configure(bg=COLOR_BG)
        print("ℹ️  Splash: transparencia no soportada, usando COLOR_BG como fondo.")

    # El color que se pintará en el lienzo (chroma o fallback)
    color_fondo = CHROMA_KEY if transparencia_activa else COLOR_BG
    fondo_rgba = _color_rgba(color_fondo)

    # ---- Crear la sombra ----
    sombra = _crear_sombra(tam_logo, SPLASH_CORNER_RADIUS)
    tam_lienzo = sombra.size  # (ancho + 2*margen, alto + 2*margen)

    # Centrar la ventana en la pantalla
    ancho, alto = tam_lienzo
    x = (splash.winfo_screenwidth() - ancho) // 2
    y = (splash.winfo_screenheight() - alto) // 2
    splash.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ---- Label para mostrar la imagen ----
    lbl_logo = tk.Label(splash, bg=color_fondo, bd=0, highlightthickness=0)
    lbl_logo.pack()
    splash._fotos = []  # evitar garbage collection

    # ---- Función de renderizado ----
    def renderizar(alpha_frac, escala_frac):
        """Pinta el logo con la transparencia y escala indicadas."""
        # Escalar el logo
        escala = ESCALA_INICIAL + (1 - ESCALA_INICIAL) * escala_frac
        nuevo_tam = (max(1, round(tam_logo[0] * escala)),
                     max(1, round(tam_logo[1] * escala)))
        logo_escalado = logo.resize(nuevo_tam, Image.Resampling.LANCZOS)

        # Aplicar fade al canal alfa del logo
        r, g, b, a = logo_escalado.split()
        a = a.point(lambda p: int(p * alpha_frac))
        logo_escalado = Image.merge("RGBA", (r, g, b, a))

        # Crear un lienzo del tamaño final, relleno con el color clave
        lienzo = Image.new("RGBA", tam_lienzo, fondo_rgba)

        # Dibujar la sombra con el mismo fade
        sombra_alpha = sombra.point(lambda p: int(p * alpha_frac))
        capa_sombra = Image.new("RGBA", tam_lienzo, (0, 0, 0, 0))
        capa_sombra.putalpha(sombra_alpha)
        lienzo = Image.alpha_composite(lienzo, capa_sombra)

        # Colocar el logo centrado sobre la sombra
        pos = ((tam_lienzo[0] - nuevo_tam[0]) // 2,
               (tam_lienzo[1] - nuevo_tam[1]) // 2)
        lienzo.paste(logo_escalado, pos, logo_escalado)

        # Convertir a PhotoImage y mostrarlo
        foto = ImageTk.PhotoImage(lienzo)
        splash._fotos = [foto]
        lbl_logo.config(image=foto)

    # ---- Función de finalización ----
    def finalizar():
        try:
            splash.destroy()
        except tk.TclError:
            pass
        al_terminar()

    # ---- Configurar la animación ----
    pasos_entrada = max(1, DURACION_ENTRADA_MS // INTERVALO_FRAME_MS)
    pasos_salida = max(1, DURACION_SALIDA_MS // INTERVALO_FRAME_MS)

    # Primer frame (totalmente invisible)
    renderizar(0.0, 0.0)
    splash.deiconify()       # mostrar ventana
    splash.lift()
    splash.focus_force()

    def animar_entrada(i=1):
        if not splash.winfo_exists():
            return
        t = _ease_out_cubic(i / float(pasos_entrada))
        renderizar(t, t)        # alpha y escala al mismo tiempo
        if i < pasos_entrada:
            splash.after(INTERVALO_FRAME_MS, lambda: animar_entrada(i + 1))
        else:
            splash.after(DURACION_ESPERA_MS, animar_salida)

    def animar_salida(i=1):
        if not splash.winfo_exists():
            finalizar()
            return
        t = i / float(pasos_salida)
        renderizar(1 - t, 1.0)  # solo fade out, escala fija
        if i < pasos_salida:
            splash.after(INTERVALO_FRAME_MS, lambda: animar_salida(i + 1))
        else:
            finalizar()

    # Iniciar la animación (ligero retraso para asegurar que la ventana está lista)
    splash.after(20, animar_entrada)