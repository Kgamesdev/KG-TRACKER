import tkinter as tk
import webbrowser
import os

class KofiModal:
    def __init__(self, parent):
        self.ventana_padre = parent
        
        self.modal = tk.Toplevel(parent)
        self.modal.withdraw()
        self.modal.title("Apoyar K Game Tracker")
        self.modal.geometry("460x280")
        self.modal.configure(bg="#1E1E2E")
        self.modal.resizable(False, False)
        self.modal.transient(parent)
        self.modal.grab_set()

        # Carga directa y certera usando logo.ico
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
                # Si fallan las rutas relativas, intentamos heredar del padre directamente
                self.modal.iconbitmap(parent.iconbitmap())
        except Exception:
            pass

        self.modal.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 460) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 280) // 2
        self.modal.geometry(f"+{x}+{y}")

        # Contenedor principal 100% unificado a #1E1E2E sin marcos extraños
        main_frame = tk.Frame(self.modal, bg="#1E1E2E")
        main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        lbl_titulo = tk.Label(
            main_frame, 
            text="☕ ¿Apoyar el proyecto?", 
            font=("Segoe UI", 14, "bold"), 
            bg="#1E1E2E", 
            fg="#ffffff"
        )
        lbl_titulo.pack(pady=(10, 10))

        lbl_desc = tk.Label(
            main_frame, 
            text="K Game Tracker es gratuito y se mantiene con esfuerzo.\n¡Invítame a un café! :)", 
            font=("Segoe UI", 10), 
            bg="#1E1E2E", 
            fg="#b0b0c0",
            justify="center",
            wraplength=400
        )
        lbl_desc.pack(pady=10)

        frame_botones = tk.Frame(main_frame, bg="#1E1E2E")
        frame_botones.pack(pady=15)

        btn_kofi = tk.Button(
            frame_botones, 
            text="Continuar a Ko-fi", 
            font=("Segoe UI", 10, "bold"), 
            bg="#FFDD00", 
            fg="#000000",
            activebackground="#e6c800",
            activeforeground="#000000",
            relief="flat",
            cursor="hand2",
            command=self.ir_a_kofi,
            padx=15,
            pady=6
        )
        btn_kofi.pack(side="left", padx=10)

        btn_cancelar = tk.Button(
            frame_botones, 
            text="Cancelar", 
            font=("Segoe UI", 10), 
            bg="#2a2a3a", 
            fg="#ffffff",
            activebackground="#3a3a4a",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.modal.destroy,
            padx=15,
            pady=6
        )
        btn_cancelar.pack(side="left", padx=10)

        self.modal.deiconify()

    def ir_a_kofi(self):
        webbrowser.open_new_tab("https://ko-fi.com/kurigamedeveloper")
        self.modal.destroy()
