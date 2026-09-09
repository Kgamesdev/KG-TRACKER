import tkinter as tk
import os

class SettingsModal:
    def __init__(self, parent):
        self.ventana_padre = parent
        
        self.modal = tk.Toplevel(parent)
        self.modal.withdraw()
        self.modal.title("Ajustes")
        self.modal.geometry("520x420")
        self.modal.configure(bg="#1E1E2E")
        self.modal.resizable(False, False)
        self.modal.transient(parent)
        self.modal.grab_set()

        # Carga del icono oficial logo.ico
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            possible_paths = [
                os.path.join(base_dir, "assets", "logo.ico"),
                os.path.join(os.getcwd(), "assets", "logo.ico"),
                "assets/logo.ico",
                "logo.ico"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    self.modal.iconbitmap(path)
                    break
            else:
                self.modal.iconbitmap(parent.iconbitmap())
        except Exception:
            pass

        self.modal.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 520) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 420) // 2
        self.modal.geometry(f"+{x}+{y}")

        # Fondo 100% unificado a #1E1E2E sin marcos ni contrastes
        main_frame = tk.Frame(self.modal, bg="#1E1E2E")
        main_frame.pack(fill="both", expand=True, padx=35, pady=25)

        # Título CENTRADO (únicamente AJUSTES)
        lbl_titulo = tk.Label(
            main_frame, 
            text="AJUSTES", 
            font=("Segoe UI", 14, "bold"), 
            bg="#1E1E2E", 
            fg="#ffffff"
        )
        lbl_titulo.pack(pady=(10, 15))

        # Línea divisoria sutil
        sep = tk.Frame(main_frame, height=1, bg="#2a2a3a")
        sep.pack(fill="x", pady=(0, 20))

        # Contenedor de opciones
        options_frame = tk.Frame(main_frame, bg="#1E1E2E")
        options_frame.pack(fill="both", expand=True)

        def crear_fila(texto, valores):
            row = tk.Frame(options_frame, bg="#1E1E2E")
            row.pack(fill="x", pady=12)
            
            lbl = tk.Label(row, text=texto, bg="#1E1E2E", fg="white", font=("Segoe UI", 11))
            lbl.pack(side="left")
            
            var = tk.StringVar(value=valores[0])
            
            # Desplegables limpios y planos acordes al tema oscuro
            menu = tk.OptionMenu(row, var, *valores)
            menu.config(
                bg="#2a2a3a", 
                fg="white", 
                activebackground="#3a3a4a", 
                activeforeground="white", 
                highlightthickness=0, 
                relief="flat", 
                font=("Segoe UI", 10),
                width=18,
                indicatoron=True
            )
            menu["menu"].config(
                bg="#2a2a3a", 
                fg="white", 
                activebackground="#5865F2", 
                activeforeground="white",
                font=("Segoe UI", 10)
            )
            menu.pack(side="right", ipadx=5, ipady=2)
            return var

        crear_fila("Idioma de la interfaz", ["Español (ES)", "English (EN)"])
        crear_fila("Tema visual", ["Neón Cyberpunk", "Oscuro Clásico", "Minimalista"])
        crear_fila("Buscar ofertas automáticamente", ["Al iniciar", "Cada hora", "Desactivado"])

        # Checkbox integrado
        chk_frame = tk.Frame(options_frame, bg="#1E1E2E")
        chk_frame.pack(fill="x", pady=12)
        
        lbl_chk = tk.Label(chk_frame, text="Iniciar minimizado con Windows", bg="#1E1E2E", fg="white", font=("Segoe UI", 11))
        lbl_chk.pack(side="left")
        
        self.chk_var = tk.IntVar()
        chk = tk.Checkbutton(
            chk_frame, 
            variable=self.chk_var, 
            bg="#1E1E2E", 
            activebackground="#1E1E2E", 
            selectcolor="#2a2a3a",
            cursor="hand2"
        )
        chk.pack(side="right")

        # Botón guardar
        btn_guardar = tk.Button(
            main_frame, 
            text="GUARDAR CAMBIOS", 
            height=2,
            bg="#5865F2", 
            fg="white",
            activebackground="#4752c4",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.guardar_y_cerrar
        )
        btn_guardar.pack(fill="x", pady=(20, 5))

        self.modal.deiconify()

    def guardar_y_cerrar(self):
        self.modal.destroy()
