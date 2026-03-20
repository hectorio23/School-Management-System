"""
Módulo de Biblioteca - Sistema Integral de Gestión Institucional (SIGI)
Frontend en Python con CustomTkinter
Conecta con el backend Django REST en http://localhost:8000/api/

Dependencias:
    pip install customtkinter requests pillow
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import requests
import json
from datetime import datetime, date
import threading

# ─── Configuración Global ───────────────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000/api"
TOKEN = None  # Se establece tras el login

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── Paleta de colores ───────────────────────────────────────────────────────
COLORS = {
    "bg":        "#0f1117",
    "surface":   "#1a1d27",
    "surface2":  "#242838",
    "border":    "#2e3347",
    "accent":    "#4ade80",   # verde – éxito / acción principal
    "accent2":   "#22d3ee",   # cian  – información
    "accent3":   "#fb923c",   # naranja – advertencia
    "danger":    "#f87171",   # rojo  – error / mora
    "warn":      "#facc15",   # amarillo – pendiente
    "text":      "#f1f5f9",
    "muted":     "#94a3b8",
    "muted2":    "#475569",
}

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEADER = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 12)
FONT_SMALL  = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 11)


# ═══════════════════════════════════════════════════════════════════════════
#  API HELPER
# ═══════════════════════════════════════════════════════════════════════════

def api_call(method: str, path: str, body: dict = None) -> dict | list | None:
    """Wrapper para llamadas HTTP al backend Django."""
    url = f"{API_BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    try:
        resp = getattr(requests, method.lower())(
            url, headers=headers,
            json=body, timeout=10
        )
        if resp.status_code == 204:
            return {}
        return resp.json()
    except requests.ConnectionError:
        messagebox.showerror("Sin conexión", "No se puede conectar al servidor.\nVerifica que el backend esté corriendo.")
        return None
    except Exception as e:
        messagebox.showerror("Error de red", str(e))
        return None


# ═══════════════════════════════════════════════════════════════════════════
#  COMPONENTES REUTILIZABLES
# ═══════════════════════════════════════════════════════════════════════════

class SectionHeader(ctk.CTkFrame):
    def __init__(self, parent, title: str, subtitle: str = "", accent_color: str = None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        color = accent_color or COLORS["accent2"]
        bar = ctk.CTkFrame(self, fg_color=color, width=4, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(0, 10))
        txt_frame = ctk.CTkFrame(self, fg_color="transparent")
        txt_frame.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(txt_frame, text=title, font=FONT_TITLE, text_color=COLORS["text"],
                     anchor="w").pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(txt_frame, text=subtitle, font=FONT_SMALL,
                         text_color=COLORS["muted"], anchor="w").pack(anchor="w")


class StatusBadge(ctk.CTkLabel):
    STATUS_MAP = {
        "prestado":  ("#fb923c", "#3b1e08"),
        "devuelto":  ("#4ade80", "#0d2618"),
        "vencido":   ("#f87171", "#2d0e0e"),
        "disponible":("#22d3ee", "#072630"),
        "pendiente": ("#facc15", "#2d2300"),
        "pagada":    ("#4ade80", "#0d2618"),
    }

    def __init__(self, parent, status: str, **kw):
        s = status.lower()
        fg, bg = self.STATUS_MAP.get(s, (COLORS["muted"], COLORS["surface2"]))
        super().__init__(parent, text=status.upper(),
                         font=FONT_MONO,
                         text_color=fg,
                         fg_color=bg,
                         corner_radius=4,
                         padx=8, pady=2, **kw)


class DataTable(ctk.CTkFrame):
    """Tabla scrolleable basada en ttk.Treeview con tema oscuro."""

    def __init__(self, parent, columns: list[tuple], on_select=None, **kw):
        super().__init__(parent, fg_color=COLORS["surface"], corner_radius=8, **kw)
        self._on_select = on_select

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                         background=COLORS["surface"],
                         foreground=COLORS["text"],
                         fieldbackground=COLORS["surface"],
                         borderwidth=0,
                         rowheight=34,
                         font=("Segoe UI", 11))
        style.configure("Custom.Treeview.Heading",
                         background=COLORS["surface2"],
                         foreground=COLORS["muted"],
                         font=("Consolas", 10, "bold"),
                         borderwidth=0,
                         relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", COLORS["surface2"])],
                  foreground=[("selected", COLORS["accent2"])])
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])

        col_ids = [c[0] for c in columns]
        self.tree = ttk.Treeview(self, columns=col_ids, show="headings",
                                  style="Custom.Treeview", selectmode="browse")

        for col_id, col_label, col_w in columns:
            self.tree.heading(col_id, text=col_label)
            self.tree.column(col_id, width=col_w, anchor="center" if col_id != "titulo" else "w",
                              stretch=col_id == "titulo")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)

        if on_select:
            self.tree.bind("<<TreeviewSelect>>", self._handle_select)

    def _handle_select(self, _event):
        sel = self.tree.selection()
        if sel and self._on_select:
            values = self.tree.item(sel[0], "values")
            self._on_select(values)

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def insert(self, values: tuple):
        self.tree.insert("", "end", values=values)

    def selected_values(self):
        sel = self.tree.selection()
        return self.tree.item(sel[0], "values") if sel else None


class FormModal(ctk.CTkToplevel):
    """Ventana modal base para formularios."""

    def __init__(self, parent, title: str, width=520, height=460):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.configure(fg_color=COLORS["bg"])
        self.grab_set()
        self.resizable(False, False)
        self.result = None

        header = ctk.CTkFrame(self, fg_color=COLORS["surface2"], corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text=title, font=FONT_HEADER,
                     text_color=COLORS["text"]).pack(pady=14, padx=20, anchor="w")

        self.body = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"])
        self.body.pack(fill="both", expand=True, padx=20, pady=10)

        self.footer = ctk.CTkFrame(self, fg_color=COLORS["surface"], height=56)
        self.footer.pack(fill="x", side="bottom")

    def add_field(self, label: str, var: tk.StringVar, placeholder="", row=0) -> ctk.CTkEntry:
        ctk.CTkLabel(self.body, text=label, font=FONT_SMALL,
                     text_color=COLORS["muted"]).pack(anchor="w", pady=(8, 2))
        entry = ctk.CTkEntry(self.body, textvariable=var, placeholder_text=placeholder,
                             fg_color=COLORS["surface2"], border_color=COLORS["border"],
                             text_color=COLORS["text"], font=FONT_BODY, height=36)
        entry.pack(fill="x")
        return entry

    def add_buttons(self, ok_text="Guardar", ok_cmd=None, cancel_cmd=None):
        ctk.CTkButton(self.footer, text="Cancelar",
                       fg_color=COLORS["surface2"], hover_color=COLORS["surface"],
                       text_color=COLORS["muted"], font=FONT_BODY,
                       command=cancel_cmd or self.destroy,
                       width=100, height=34).pack(side="right", padx=(4, 12), pady=11)
        ctk.CTkButton(self.footer, text=ok_text,
                       fg_color=COLORS["accent"], hover_color="#22c55e",
                       text_color="#0f1117", font=("Segoe UI", 12, "bold"),
                       command=ok_cmd,
                       width=120, height=34).pack(side="right", padx=4, pady=11)


# ═══════════════════════════════════════════════════════════════════════════
#  VISTAS
# ═══════════════════════════════════════════════════════════════════════════

class InventarioView(ctk.CTkFrame):
    """Vista de inventario de libros con CRUD completo."""

    COLUMNS = [
        ("id",        "ID",       50),
        ("titulo",    "Título",   260),
        ("autor",     "Autor",    160),
        ("isbn",      "ISBN",     130),
        ("total",     "Total",    60),
        ("prestados", "Prestados",80),
        ("disp",      "Disp.",    60),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ── Encabezado
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        SectionHeader(top, "Inventario de Libros", "Catálogo completo del acervo",
                      accent_color=COLORS["accent2"]).pack(side="left")
        ctk.CTkButton(top, text="＋  Agregar libro",
                       fg_color=COLORS["accent"], hover_color="#22c55e",
                       text_color="#0f1117", font=("Segoe UI", 12, "bold"),
                       command=self.modal_agregar, height=36).pack(side="right")

        # ── Barra de búsqueda
        search_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=8)
        search_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 14),
                     text_color=COLORS["muted"]).pack(side="left", padx=(12, 4))
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._filter())
        ctk.CTkEntry(search_frame, textvariable=self._search_var,
                     placeholder_text="Buscar por título o autor...",
                     fg_color="transparent", border_width=0,
                     text_color=COLORS["text"], font=FONT_BODY,
                     height=40).pack(fill="x", padx=4)

        # ── Tabla
        self.table = DataTable(self, self.COLUMNS, on_select=self._on_select)
        self.table.pack(fill="both", expand=True)

        # ── Botones de acción (se activan al seleccionar fila)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=(10, 0))
        self.btn_edit = ctk.CTkButton(self.btn_frame, text="✏  Editar",
                                       fg_color=COLORS["surface2"], hover_color=COLORS["border"],
                                       text_color=COLORS["text"], font=FONT_BODY,
                                       state="disabled", command=self.modal_editar, height=34)
        self.btn_edit.pack(side="left", padx=(0, 8))
        self.btn_del = ctk.CTkButton(self.btn_frame, text="🗑  Eliminar",
                                      fg_color=COLORS["surface2"], hover_color="#3b0d0d",
                                      text_color=COLORS["danger"], font=FONT_BODY,
                                      state="disabled", command=self.eliminar, height=34)
        self.btn_del.pack(side="left")

        self._selected = None
        self._all_data = []

    def _on_select(self, values):
        self._selected = values
        self.btn_edit.configure(state="normal")
        self.btn_del.configure(state="normal")

    def refresh(self):
        self.table.clear()
        data = api_call("GET", "/biblioteca/libros/") or []
        if isinstance(data, dict):
            data = data.get("results", [])
        self._all_data = data
        for libro in data:
            disp = libro.get("numero_de_ejemplares", 0) - libro.get("numero_de_ejemplares_prestados", 0)
            self.table.insert((
                libro.get("id", ""),
                libro.get("titulo", ""),
                libro.get("autor", ""),
                libro.get("isbn", ""),
                libro.get("numero_de_ejemplares", 0),
                libro.get("numero_de_ejemplares_prestados", 0),
                disp,
            ))

    def _filter(self):
        q = self._search_var.get().lower()
        self.table.clear()
        for libro in self._all_data:
            if q in libro.get("titulo", "").lower() or q in libro.get("autor", "").lower():
                disp = libro.get("numero_de_ejemplares", 0) - libro.get("numero_de_ejemplares_prestados", 0)
                self.table.insert((
                    libro.get("id", ""),
                    libro.get("titulo", ""),
                    libro.get("autor", ""),
                    libro.get("isbn", ""),
                    libro.get("numero_de_ejemplares", 0),
                    libro.get("numero_de_ejemplares_prestados", 0),
                    disp,
                ))

    def modal_agregar(self):
        m = FormModal(self, "Agregar Libro", height=500)
        v_titulo = tk.StringVar()
        v_autor  = tk.StringVar()
        v_isbn   = tk.StringVar()
        v_cant   = tk.StringVar(value="1")
        m.add_field("Título *", v_titulo, "Nombre del libro")
        m.add_field("Autor *", v_autor, "Nombre del autor")
        m.add_field("ISBN", v_isbn, "978-XXXXXXXXXX")
        m.add_field("Número de ejemplares", v_cant, "1")

        def guardar():
            if not v_titulo.get() or not v_autor.get():
                messagebox.showwarning("Campos requeridos", "Título y Autor son obligatorios.", parent=m)
                return
            body = {
                "titulo": v_titulo.get(),
                "autor": v_autor.get(),
                "isbn": v_isbn.get(),
                "numero_de_ejemplares": int(v_cant.get() or 1),
            }
            r = api_call("POST", "/biblioteca/libros/", body)
            if r and "id" in r:
                messagebox.showinfo("Éxito", f"Libro '{r['titulo']}' registrado.", parent=m)
                m.destroy()
                self.refresh()
            elif r:
                messagebox.showerror("Error", str(r), parent=m)

        m.add_buttons("Guardar", ok_cmd=guardar, cancel_cmd=m.destroy)

    def modal_editar(self):
        if not self._selected:
            return
        libro_id = self._selected[0]
        m = FormModal(self, "Editar Libro", height=500)
        v_titulo = tk.StringVar(value=self._selected[1])
        v_autor  = tk.StringVar(value=self._selected[2])
        v_isbn   = tk.StringVar(value=self._selected[3])
        v_cant   = tk.StringVar(value=str(self._selected[4]))
        m.add_field("Título *", v_titulo)
        m.add_field("Autor *", v_autor)
        m.add_field("ISBN", v_isbn)
        m.add_field("Número de ejemplares", v_cant)

        def guardar():
            body = {
                "titulo": v_titulo.get(),
                "autor": v_autor.get(),
                "isbn": v_isbn.get(),
                "numero_de_ejemplares": int(v_cant.get() or 1),
            }
            r = api_call("PUT", f"/biblioteca/libros/{libro_id}/", body)
            if r:
                messagebox.showinfo("Éxito", "Libro actualizado.", parent=m)
                m.destroy()
                self.refresh()

        m.add_buttons("Actualizar", ok_cmd=guardar, cancel_cmd=m.destroy)

    def eliminar(self):
        if not self._selected:
            return
        libro_id, titulo = self._selected[0], self._selected[1]
        if messagebox.askyesno("Confirmar eliminación",
                               f"¿Eliminar el libro '{titulo}'?\nEsta acción no se puede deshacer."):
            api_call("DELETE", f"/biblioteca/libros/{libro_id}/")
            self.refresh()
            self.btn_edit.configure(state="disabled")
            self.btn_del.configure(state="disabled")


# ─────────────────────────────────────────────────────────────────────────────

class PrestamosView(ctk.CTkFrame):
    """Vista de préstamos activos y registro de nuevos préstamos / devoluciones."""

    COLUMNS = [
        ("id",          "ID",       50),
        ("libro",       "Libro",    220),
        ("usuario",     "Usuario",  160),
        ("salida",      "Salida",   110),
        ("vencimiento", "Vence",    110),
        ("estado",      "Estado",    90),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        SectionHeader(top, "Préstamos Activos", "Libros actualmente en circulación",
                      accent_color=COLORS["accent3"]).pack(side="left")
        ctk.CTkButton(top, text="＋  Nuevo préstamo",
                       fg_color=COLORS["accent3"], hover_color="#ea580c",
                       text_color="#fff", font=("Segoe UI", 12, "bold"),
                       command=self.modal_prestamo, height=36).pack(side="right")

        # Filtros rápidos
        filt = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=8)
        filt.pack(fill="x", pady=(0, 10))
        self._filter_var = tk.StringVar(value="todos")
        for val, label in [("todos", "Todos"), ("prestado", "Prestados"), ("vencido", "Vencidos"), ("devuelto", "Devueltos")]:
            ctk.CTkRadioButton(filt, text=label, variable=self._filter_var, value=val,
                                fg_color=COLORS["accent2"], text_color=COLORS["muted"],
                                font=FONT_SMALL, command=self.refresh).pack(side="left", padx=14, pady=8)

        self.table = DataTable(self, self.COLUMNS, on_select=self._on_select)
        self.table.pack(fill="both", expand=True)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        self.btn_dev = ctk.CTkButton(btn_frame, text="↩  Registrar devolución",
                                      fg_color=COLORS["accent"], hover_color="#22c55e",
                                      text_color="#0f1117", font=("Segoe UI", 12, "bold"),
                                      state="disabled", command=self.devolver, height=36)
        self.btn_dev.pack(side="left")

        self._selected = None
        self._all_data = []

    def _on_select(self, values):
        self._selected = values
        # Solo habilitar devolución si estado == prestado
        self.btn_dev.configure(state="normal" if values[5].lower() == "prestado" else "disabled")

    def refresh(self):
        self.table.clear()
        filtro = self._filter_var.get() if hasattr(self, "_filter_var") else "todos"
        path = "/biblioteca/prestamos/"
        if filtro != "todos":
            path += f"?estado={filtro}"
        data = api_call("GET", path) or []
        if isinstance(data, dict):
            data = data.get("results", [])
        self._all_data = data
        for p in data:
            self.table.insert((
                p.get("id", ""),
                p.get("libro_titulo", p.get("libro", "")),
                p.get("usuario_nombre", p.get("usuario", "")),
                p.get("fecha_salida", ""),
                p.get("fecha_de_devolucion", ""),
                p.get("estado", ""),
            ))

    def modal_prestamo(self):
        m = FormModal(self, "Registrar Préstamo", height=460)
        v_libro   = tk.StringVar()
        v_usuario = tk.StringVar()
        v_vence   = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        m.add_field("ID del Libro *", v_libro, "Número de ID del libro")
        m.add_field("ID o matrícula del usuario *", v_usuario, "Matrícula o ID del alumno/maestro")
        m.add_field("Fecha de devolución (YYYY-MM-DD)", v_vence)

        def guardar():
            if not v_libro.get() or not v_usuario.get():
                messagebox.showwarning("Campos requeridos", "Libro y Usuario son obligatorios.", parent=m)
                return
            body = {
                "libro": v_libro.get(),
                "usuario": v_usuario.get(),
                "fecha_de_devolucion": v_vence.get(),
            }
            r = api_call("POST", "/biblioteca/prestamos/", body)
            if r and "id" in r:
                messagebox.showinfo("Préstamo registrado",
                                    f"Préstamo #{r['id']} creado exitosamente.", parent=m)
                m.destroy()
                self.refresh()
            elif r:
                messagebox.showerror("Error", str(r), parent=m)

        m.add_buttons("Registrar", ok_cmd=guardar, cancel_cmd=m.destroy)

    def devolver(self):
        if not self._selected:
            return
        pid = self._selected[0]
        if messagebox.askyesno("Confirmar devolución",
                               f"¿Registrar devolución del préstamo #{pid}?\n"
                               "Se actualizará el stock del libro automáticamente."):
            r = api_call("PATCH", f"/biblioteca/prestamos/{pid}/devolver/")
            if r is not None:
                messagebox.showinfo("Devolución registrada",
                                    "El libro fue devuelto correctamente.")
                self.refresh()
                self.btn_dev.configure(state="disabled")


# ─────────────────────────────────────────────────────────────────────────────

class MultasView(ctk.CTkFrame):
    """Vista de multas por retraso."""

    COLUMNS = [
        ("id",       "ID",        50),
        ("prestamo", "Préstamo",  80),
        ("usuario",  "Usuario",   180),
        ("dias",     "Días retr.", 90),
        ("monto",    "Monto",     90),
        ("estado",   "Estado",    100),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        SectionHeader(top, "Multas por Retraso", "Sanciones económicas pendientes y pagadas",
                      accent_color=COLORS["danger"]).pack(side="left")

        self.table = DataTable(self, self.COLUMNS, on_select=self._on_select)
        self.table.pack(fill="both", expand=True)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        self.btn_pagar = ctk.CTkButton(btn_frame, text="💳  Registrar pago de multa",
                                        fg_color=COLORS["accent"], hover_color="#22c55e",
                                        text_color="#0f1117", font=("Segoe UI", 12, "bold"),
                                        state="disabled", command=self.pagar, height=36)
        self.btn_pagar.pack(side="left")
        self._selected = None

    def _on_select(self, values):
        self._selected = values
        self.btn_pagar.configure(state="normal" if values[5].lower() == "pendiente" else "disabled")

    def refresh(self):
        self.table.clear()
        data = api_call("GET", "/biblioteca/multas/") or []
        if isinstance(data, dict):
            data = data.get("results", [])
        for m in data:
            self.table.insert((
                m.get("id", ""),
                m.get("prestamo", ""),
                m.get("usuario_nombre", ""),
                m.get("dias_retraso", 0),
                f"${m.get('monto', 0):.2f}",
                m.get("estado", "pendiente"),
            ))

    def pagar(self):
        if not self._selected:
            return
        mid = self._selected[0]
        if messagebox.askyesno("Confirmar pago", f"¿Registrar pago de la multa #{mid}?"):
            r = api_call("PATCH", f"/biblioteca/multas/{mid}/pagar/")
            if r is not None:
                messagebox.showinfo("Pago registrado", "Multa marcada como pagada.")
                self.refresh()


# ─────────────────────────────────────────────────────────────────────────────

class MisPrestamosView(ctk.CTkFrame):
    """Vista de préstamos propios (para usuarios alumno/maestro)."""

    COLUMNS = [
        ("id",          "ID",     50),
        ("libro",       "Libro",  260),
        ("salida",      "Salida", 120),
        ("vencimiento", "Vence",  120),
        ("estado",      "Estado",  90),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        SectionHeader(top, "Mis Préstamos", "Libros actualmente a tu cargo",
                      accent_color=COLORS["accent"]).pack(side="left")
        ctk.CTkButton(top, text="↻  Actualizar",
                       fg_color=COLORS["surface2"], hover_color=COLORS["border"],
                       text_color=COLORS["muted"], font=FONT_BODY,
                       command=self.refresh, height=32).pack(side="right")

        self.table = DataTable(self, self.COLUMNS)
        self.table.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.table.clear()
        data = api_call("GET", "/biblioteca/mis-prestamos/") or []
        if isinstance(data, dict):
            data = data.get("results", [])
        for p in data:
            self.table.insert((
                p.get("id", ""),
                p.get("libro_titulo", ""),
                p.get("fecha_salida", ""),
                p.get("fecha_de_devolucion", ""),
                p.get("estado", ""),
            ))


# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

class SidebarButton(ctk.CTkButton):
    def __init__(self, parent, text, icon, command, **kw):
        super().__init__(parent, text=f"  {icon}  {text}",
                         fg_color="transparent",
                         hover_color=COLORS["surface2"],
                         anchor="w",
                         text_color=COLORS["muted"],
                         font=("Segoe UI", 12),
                         height=40,
                         corner_radius=6,
                         command=command, **kw)
        self._active = False

    def set_active(self, active: bool):
        self._active = active
        if active:
            self.configure(fg_color=COLORS["surface2"], text_color=COLORS["text"])
        else:
            self.configure(fg_color="transparent", text_color=COLORS["muted"])


# ═══════════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

class BibliotecaApp(ctk.CTk):
    VIEWS = [
        ("inventario",   "Inventario",    "📚", InventarioView),
        ("prestamos",    "Préstamos",     "🔄", PrestamosView),
        ("multas",       "Multas",        "⚠️", MultasView),
        ("mis_prestamos","Mis préstamos", "👤", MisPrestamosView),
    ]

    def __init__(self):
        super().__init__()
        self.title("Biblioteca · SIGI-CEJLG")
        self.geometry("1200x700")
        self.configure(fg_color=COLORS["bg"])
        self.minsize(900, 580)
        self._active_view = None
        self._sidebar_btns = {}
        self._view_cache = {}
        self._build_layout()
        self.switch_view("inventario")

    def _build_layout(self):
        # ── Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["surface"],
                                     width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / Título sistema
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["surface2"], corner_radius=0, height=60)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(logo_frame, text="📖  Biblioteca",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["text"]).pack(pady=18, padx=18, anchor="w")

        ctk.CTkLabel(self.sidebar, text="MÓDULO", font=("Consolas", 9),
                     text_color=COLORS["muted2"]).pack(anchor="w", padx=16, pady=(18, 4))

        for key, label, icon, _cls in self.VIEWS:
            btn = SidebarButton(self.sidebar, label, icon,
                                 command=lambda k=key: self.switch_view(k))
            btn.pack(fill="x", padx=8, pady=2)
            self._sidebar_btns[key] = btn

        # Separador
        ctk.CTkFrame(self.sidebar, fg_color=COLORS["border"], height=1).pack(fill="x", pady=12, padx=12)

        # Indicador de conexión
        self._conn_label = ctk.CTkLabel(self.sidebar, text="⚡ Conectando…",
                                         font=FONT_SMALL, text_color=COLORS["warn"])
        self._conn_label.pack(anchor="w", padx=16, pady=4)
        self._check_connection()

        # ── Content
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def _check_connection(self):
        def _check():
            r = api_call("GET", "/biblioteca/libros/")
            if r is not None:
                self._conn_label.configure(text="🟢 Conectado", text_color=COLORS["accent"])
            else:
                self._conn_label.configure(text="🔴 Sin conexión", text_color=COLORS["danger"])
        threading.Thread(target=_check, daemon=True).start()

    def switch_view(self, key: str):
        # Ocultar vista activa
        if self._active_view:
            self._active_view.pack_forget()
            for k, b in self._sidebar_btns.items():
                b.set_active(False)

        # Crear o recuperar vista
        if key not in self._view_cache:
            cls = next(c for k, _, _, c in self.VIEWS if k == key)
            self._view_cache[key] = cls(self.content)

        self._active_view = self._view_cache[key]
        self._active_view.pack(fill="both", expand=True)
        self._sidebar_btns[key].set_active(True)


# ═══════════════════════════════════════════════════════════════════════════
#  PANTALLA DE LOGIN
# ═══════════════════════════════════════════════════════════════════════════

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIGI · Acceso Biblioteca")
        self.geometry("440x520")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        card = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=12)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.82)

        # Encabezado
        ctk.CTkLabel(card, text="📖", font=("Segoe UI", 42)).pack(pady=(32, 4))
        ctk.CTkLabel(card, text="Sistema de Biblioteca",
                     font=("Segoe UI", 16, "bold"), text_color=COLORS["text"]).pack()
        ctk.CTkLabel(card, text="SIGI · CEJLG",
                     font=FONT_SMALL, text_color=COLORS["muted"]).pack(pady=(2, 24))

        # Campos
        self._email_var = tk.StringVar()
        self._pass_var  = tk.StringVar()

        for label, var, show in [("Correo electrónico", self._email_var, ""),
                                  ("Contraseña", self._pass_var, "●")]:
            ctk.CTkLabel(card, text=label, font=FONT_SMALL,
                         text_color=COLORS["muted"], anchor="w").pack(fill="x", padx=28, pady=(8, 2))
            e = ctk.CTkEntry(card, textvariable=var, show=show,
                              fg_color=COLORS["surface2"], border_color=COLORS["border"],
                              text_color=COLORS["text"], font=FONT_BODY, height=38)
            e.pack(fill="x", padx=28)

        self._msg = ctk.CTkLabel(card, text="", font=FONT_SMALL, text_color=COLORS["danger"])
        self._msg.pack(pady=(10, 0))

        ctk.CTkButton(card, text="Iniciar sesión",
                       fg_color=COLORS["accent"], hover_color="#22c55e",
                       text_color="#0f1117", font=("Segoe UI", 13, "bold"),
                       command=self._login, height=40).pack(fill="x", padx=28, pady=(12, 0))

        # Botón demo (sin credenciales reales)
        ctk.CTkButton(card, text="Entrar sin autenticación (demo)",
                       fg_color="transparent", hover_color=COLORS["surface2"],
                       text_color=COLORS["muted"], font=FONT_SMALL,
                       command=self._skip_login).pack(pady=(8, 0))

        self._pass_var  # Keep reference

    def _login(self):
        email = self._email_var.get().strip()
        pwd   = self._pass_var.get()
        if not email or not pwd:
            self._msg.configure(text="Completa todos los campos.")
            return
        self._msg.configure(text="Verificando…", text_color=COLORS["warn"])
        self.update()

        r = api_call("POST", "/token/", {"email": email, "password": pwd})
        if r and "access" in r:
            global TOKEN
            TOKEN = r["access"]
            self._open_app()
        elif r and r.get("mfa_required"):
            self._msg.configure(text="Se requiere MFA. Ingresa el código enviado al correo.",
                                 text_color=COLORS["warn"])
            self._ask_mfa(email)
        else:
            self._msg.configure(text="Credenciales incorrectas.", text_color=COLORS["danger"])

    def _ask_mfa(self, email: str):
        w = FormModal(self, "Verificación MFA", height=320)
        v_code = tk.StringVar()
        w.add_field("Código de 6 dígitos", v_code, "XXXXXX")

        def verify():
            r = api_call("POST", "/users/mfa/verify/", {"email": email, "code": v_code.get()})
            if r and "access" in r:
                global TOKEN
                TOKEN = r["access"]
                w.destroy()
                self._open_app()
            else:
                messagebox.showerror("Código incorrecto", "El código no es válido o expiró.", parent=w)

        w.add_buttons("Verificar", ok_cmd=verify, cancel_cmd=w.destroy)

    def _skip_login(self):
        self._open_app()

    def _open_app(self):
        self.destroy()
        app = BibliotecaApp()
        app.mainloop()


# ═══════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    BibliotecaApp().mainloop()
