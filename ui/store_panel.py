"""Panel de tiendas con estilo tipo botones iOS e insignias de notificación.

Nota: Este módulo proporciona un widget reutilizable que puede integrarse
en futuras versiones. Actualmente, la lógica está en main_window.py
"""

import tkinter as tk
from config import (
    COLOR_BG, COLOR_BG_CARD, COLOR_ACCENT, COLOR_ACCENT_LIGHT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_SUCCESS_HOVER
)


class StorePanel(tk.Frame):
    """
    Panel de tiendas con burbujas interactivas y insignias de notificación.
    
    Ejemplo de uso:
        panel = StorePanel(
            parent_frame,
            store_names=["Steam", "Epic Games", "GOG"],
            on_store_click=mi_funcion_callback
        )
        panel.pack()
        panel.actualizar_conteos({"Steam": 5, "Epic Games": 3})
    """

    def __init__(self, parent, store_names, on_store_click=None):
        """
        Inicializa el panel de tiendas.
        
        Args:
            parent (tk.Widget): Widget padre
            store_names (list): Lista de nombres de tiendas
            on_store_click (callable): Función callback al hacer click en una tienda
                                       Recibe (nombre_tienda, es_activo)
        """
        super().__init__(parent, bg=COLOR_BG)
        
        self.store_names = store_names
        self.on_store_click = on_store_click
        
        # Estado de cada tienda
        self.active_filters = {store: True for store in store_names}
        self.store_counts = {store: 0 for store in store_names}
        
        # Widgets almacenados por tienda
        self.circles = {}      # {tienda: (canvas, circle_id, label)}
        self.badges = {}       # {tienda: (badge_bg, badge_text)}
        
        self._build_panel()

    def _build_panel(self):
        """Construye el panel visual con las burbujas de tiendas."""
        # Container para los botones en fila
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(expand=True)

        # Iconos/emojis para cada tienda
        icons = {
            "Steam": "🎮",
            "Epic Games": "⚡",
            "GOG": "👾",
            "Amazon Prime": "🎁",
            "Humble Store": "💎",
            "Itch.io": "🕹️",
            "Fanatical": "🎯",
            "IndieGala": "🎪",
            "Otras Plataformas": "💻"
        }

        # Crear burbuja para cada tienda
        for store in self.store_names:
            item_frame = tk.Frame(container, bg=COLOR_BG, cursor="hand2")
            item_frame.pack(side="left", padx=10)

            # Canvas circular
            canvas = tk.Canvas(
                item_frame,
                width=54,
                height=54,
                bg=COLOR_BG,
                highlightthickness=0
            )
            canvas.pack()

            # Círculo base
            circle_id = canvas.create_oval(
                3, 3, 51, 51,
                fill=COLOR_BG_CARD,
                outline=COLOR_ACCENT,
                width=2
            )
            
            # Icono/emoji
            icon_text = icons.get(store, "🎮")
            canvas.create_text(
                27, 27,
                text=icon_text,
                font=("Segoe UI Emoji", 18)
            )

            # Insignia roja de notificación (número de ofertas)
            badge_bg = canvas.create_oval(
                34, 2, 52, 20,
                fill="#FF3B30",
                outline="white",
                width=1,
                state="hidden"
            )
            badge_text = canvas.create_text(
                43, 11,
                text="0",
                fill="white",
                font=("Arial", 8, "bold"),
                state="hidden"
            )

            # Etiqueta con nombre de tienda
            lbl_name = tk.Label(
                item_frame,
                text=store,
                font=("Arial", 8, "bold"),
                bg=COLOR_BG,
                fg=COLOR_TEXT_PRIMARY
            )
            lbl_name.pack(pady=(4, 0))

            # Guardar referencias
            self.circles[store] = (canvas, circle_id, lbl_name)
            self.badges[store] = (badge_bg, badge_text)

            # Eventos de interacción
            for widget in (canvas, item_frame, lbl_name):
                widget.bind("<Button-1>", lambda e, s=store: self._toggle_store(s))
                widget.bind("<Enter>", lambda e, s=store: self._on_hover(s, True))
                widget.bind("<Leave>", lambda e, s=store: self._on_hover(s, False))

    def _on_hover(self, store_name, is_hovering):
        """Efecto visual al pasar el ratón sobre una tienda."""
        canvas, circle_id, _ = self.circles[store_name]
        
        if is_hovering:
            canvas.itemconfig(circle_id, outline=COLOR_ACCENT_LIGHT, width=3)
        else:
            is_active = self.active_filters[store_name]
            color = COLOR_SUCCESS if is_active else COLOR_ACCENT
            width = 3 if is_active else 2
            canvas.itemconfig(circle_id, outline=color, width=width)

    def _toggle_store(self, store_name):
        """Alterna el estado de una tienda (activa/inactiva)."""
        is_active = not self.active_filters[store_name]
        self.active_filters[store_name] = is_active
        
        canvas, circle_id, lbl_name = self.circles[store_name]
        
        if is_active:
            # Tienda activa: verde
            canvas.itemconfig(circle_id, outline=COLOR_SUCCESS, fill=COLOR_BG_CARD)
            lbl_name.config(fg=COLOR_SUCCESS)
        else:
            # Tienda inactiva: gris
            canvas.itemconfig(circle_id, outline=COLOR_TEXT_MUTED, fill=COLOR_BG_CARD)
            lbl_name.config(fg=COLOR_TEXT_MUTED)

        # Llamar callback si existe
        if self.on_store_click:
            self.on_store_click(store_name, is_active)

    def actualizar_conteos(self, conteos_dict):
        """
        Actualiza los números en las insignias de notificación.
        
        Args:
            conteos_dict (dict): Diccionario {nombre_tienda: cantidad}
            
        Ejemplo:
            panel.actualizar_conteos({"Steam": 5, "Epic Games": 3})
        """
        for store_name, count in conteos_dict.items():
            if store_name not in self.badges:
                continue

            badge_bg, badge_text = self.badges[store_name]
            canvas, _, _ = self.circles[store_name]
            
            if count > 0:
                # Mostrar insignia
                canvas.itemconfig(badge_text, text=str(count))
                canvas.itemconfig(badge_bg, state="normal")
                canvas.itemconfig(badge_text, state="normal")
            else:
                # Ocultar insignia
                canvas.itemconfig(badge_bg, state="hidden")
                canvas.itemconfig(badge_text, state="hidden")

    def obtener_tiendas_activas(self):
        """
        Retorna una lista de tiendas activas.
        
        Returns:
            list: Nombres de tiendas seleccionadas
            
        Ejemplo:
            tiendas = panel.obtener_tiendas_activas()
            # Resultado: ["Steam", "Epic Games"]
        """
        return [s for s, activo in self.active_filters.items() if activo]

    def establecer_tienda_activa(self, store_name, activo):
        """
        Establece manualmente si una tienda está activa o no.
        
        Args:
            store_name (str): Nombre de la tienda
            activo (bool): True para activar, False para desactivar
            
        Ejemplo:
            panel.establecer_tienda_activa("Steam", False)
        """
        self.active_filters[store_name] = activo
        canvas, circle_id, lbl_name = self.circles[store_name]
        
        if activo:
            canvas.itemconfig(circle_id, outline=COLOR_SUCCESS)
            lbl_name.config(fg=COLOR_SUCCESS)
        else:
            canvas.itemconfig(circle_id, outline=COLOR_TEXT_MUTED)
            lbl_name.config(fg=COLOR_TEXT_MUTED)