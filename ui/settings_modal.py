import customtkinter as ctk

class SettingsModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Ajustes de Configuración")
        self.geometry("600x500")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.configure(fg_color="#121218")
        
        main_frame = ctk.CTkFrame(self, fg_color="#1a1a24", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="AJUSTES DE CONFIGURACIÓN", 
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left")
        
        btn_close = ctk.CTkButton(
            header_frame, 
            text="✕", 
            width=30, 
            height=30,
            fg_color="transparent", 
            hover_color="#2a2a3a",
            text_color="white",
            command=self.destroy
        )
        btn_close.pack(side="right")
        
        sep = ctk.CTkFrame(main_frame, height=2, fg_color="#2a2a3a")
        sep.pack(fill="x", padx=20, pady=10)
        
        options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.crear_fila_opcion(options_frame, "Idioma de la interfaz", ["Español (ES)", "English (EN)"], 0)
        self.crear_fila_opcion(options_frame, "Tema visual", ["Neón Cyberpunk", "Oscuro Clásico", "Minimalista"], 0)
        self.crear_fila_opcion(options_frame, "Buscar ofertas automáticamente", ["Al iniciar", "Cada hora", "Desactivado"], 0)
        
        chk_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        chk_frame.pack(fill="x", pady=12)
        
        lbl_chk = ctk.CTkLabel(chk_frame, text="Iniciar minimizado con Windows", text_color="white", font=ctk.CTkFont(size=13))
        lbl_chk.pack(side="left")
        
        self.chk_iniciar = ctk.CTkCheckBox(chk_frame, text="", width=24, fg_color="#5865F2", hover_color="#4752C4")
        self.chk_iniciar.pack(side="right")
        
        btn_guardar = ctk.CTkButton(
            main_frame, 
            text="GUARDAR CAMBIOS", 
            height=40,
            fg_color="#5865F2", 
            hover_color="#4752C4",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.guardar_y_cerrar
        )
        btn_guardar.pack(fill="x", padx=20, pady=(10, 20))

    def crear_fila_opcion(self, parent, texto, valores, default_index):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=10)
        
        lbl = ctk.CTkLabel(row, text=texto, text_color="white", font=ctk.CTkFont(size=13))
        lbl.pack(side="left")
        
        combo = ctk.CTkComboBox(row, values=valores, width=160, fg_color="#121218", button_color="#5865F2", button_hover_color="#4752C4", border_color="#2a2a3a")
        combo.set(valores[default_index])
        combo.pack(side="right")
        return combo

    def guardar_y_cerrar(self):
        self.destroy()
