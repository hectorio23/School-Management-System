import customtkinter as ctk

class DashboardUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#2c3e50")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="Library Sys", font=("Arial", 24, "bold"),
                     text_color="white").pack(pady=30)
        
        self.btn_inventario = self.crear_boton_menu("📚 Inventario")
        self.btn_prestamos = self.crear_boton_menu("📂 Préstamos")
        self.btn_admin = self.crear_boton_menu("⚙ Administrar Biblioteca")
        
        self.content = ctk.CTkFrame(self, fg_color="#f5f6fa")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.entry_busqueda = ctk.CTkEntry(self.content, placeholder_text="Buscar libro...", height=45)
        self.entry_busqueda.pack(fill="x", pady=20)

        self.tabla_scroll = ctk.CTkScrollableFrame(self.content, fg_color="white", label_text="Listado")
        self.tabla_scroll.pack(fill="both", expand=True)

    def crear_boton_menu(self, texto):
        btn = ctk.CTkButton(self.sidebar, text=texto, fg_color="transparent",
                            anchor="w", hover_color="#34495e")
        btn.pack(fill="x", padx=20, pady=10)
        return btn

    def preparar_tabla(self, titulo_seccion):
        for widget in self.tabla_scroll.winfo_children():
            widget.destroy()
        self.tabla_scroll.configure(label_text=titulo_seccion)
