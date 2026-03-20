"""
Módulo de Comedor - Sistema Integral de Gestión Institucional (SIGI)
Frontend en Python con CustomTkinter
Conecta con el backend Django REST en http://localhost:8000/api/

Dependencias:
    pip install customtkinter requests pillow

Endpoints que consume:
    GET/POST        /api/comedor/admin/asistencias/
    DELETE          /api/comedor/admin/asistencias/{id}/
    GET/POST        /api/comedor/admin/menus/
    PUT             /api/comedor/admin/menus/{id}/
    GET             /api/comedor/menu/           (portal alumno)
    POST            /api/token/
    POST            /api/users/mfa/verify/
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import date, datetime
import threading
import requests

# ─── Configuración Global ───────────────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000/api"
TOKEN    = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── Paleta ─────────────────────────────────────────────────────────────────
C = {
    "bg":       "#0e1014",
    "surface":  "#181b22",
    "surface2": "#21262f",
    "border":   "#2b3040",
    "accent":   "#4ade80",   # verde
    "accent2":  "#22d3ee",   # cian
    "accent3":  "#fb923c",   # naranja (comedor)
    "accent4":  "#a78bfa",   # morado
    "danger":   "#f87171",
    "warn":     "#facc15",
    "text":     "#f1f5f9",
    "muted":    "#94a3b8",
    "muted2":   "#3f4a5c",
}

FT = ("Segoe UI", 20, "bold")
FH = ("Segoe UI", 13, "bold")
FB = ("Segoe UI", 12)
FS = ("Segoe UI", 10)
FM = ("Consolas", 11)


# ═══════════════════════════════════════════════════════════════════════════
#  API HELPER
# ═══════════════════════════════════════════════════════════════════════════

def api(method: str, path: str, body=None):
    url = f"{API_BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    try:
        r = getattr(requests, method.lower())(url, headers=headers, json=body, timeout=10)
        if r.status_code == 204:
            return {}
        return r.json()
    except requests.ConnectionError:
        messagebox.showerror("Sin conexión", "No se puede alcanzar el servidor.\nVerifica que el backend esté activo.")
        return None
    except Exception as e:
        messagebox.showerror("Error de red", str(e))
        return None


# ═══════════════════════════════════════════════════════════════════════════
#  WIDGETS REUTILIZABLES
# ═══════════════════════════════════════════════════════════════════════════

class SectionHeader(ctk.CTkFrame):
    def __init__(self, parent, title, subtitle="", color=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        bar = ctk.CTkFrame(self, fg_color=color or C["accent3"], width=4, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(0, 10))
        tf = ctk.CTkFrame(self, fg_color="transparent")
        tf.pack(side="left")
        ctk.CTkLabel(tf, text=title, font=FT, text_color=C["text"], anchor="w").pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(tf, text=subtitle, font=FS, text_color=C["muted"], anchor="w").pack(anchor="w")


class DataTable(ctk.CTkFrame):
    def __init__(self, parent, columns, on_select=None, **kw):
        super().__init__(parent, fg_color=C["surface"], corner_radius=8, **kw)
        self._on_select = on_select

        s = ttk.Style()
        s.theme_use("clam")
        s.configure("T.Treeview",
                    background=C["surface"], foreground=C["text"],
                    fieldbackground=C["surface"], borderwidth=0,
                    rowheight=34, font=("Segoe UI", 11))
        s.configure("T.Treeview.Heading",
                    background=C["surface2"], foreground=C["muted"],
                    font=("Consolas", 10, "bold"), borderwidth=0, relief="flat")
        s.map("T.Treeview",
              background=[("selected", C["surface2"])],
              foreground=[("selected", C["accent2"])])
        s.layout("T.Treeview", [("T.Treeview.treearea", {"sticky": "nswe"})])

        col_ids = [c[0] for c in columns]
        self.tree = ttk.Treeview(self, columns=col_ids, show="headings",
                                  style="T.Treeview", selectmode="browse")
        for cid, clabel, cw in columns:
            self.tree.heading(cid, text=clabel)
            self.tree.column(cid, width=cw,
                              anchor="w" if cid in ("desc", "notas", "titulo") else "center",
                              stretch=cid in ("desc", "notas", "titulo"))

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)

        if on_select:
            self.tree.bind("<<TreeviewSelect>>", lambda _: on_select(self.selected()))

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def insert(self, values):
        self.tree.insert("", "end", values=values)

    def selected(self):
        sel = self.tree.selection()
        return self.tree.item(sel[0], "values") if sel else None


class Modal(ctk.CTkToplevel):
    def __init__(self, parent, title, w=520, h=480):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{w}x{h}")
        self.configure(fg_color=C["bg"])
        self.grab_set()
        self.resizable(False, False)

        hdr = ctk.CTkFrame(self, fg_color=C["surface2"], corner_radius=0)
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=title, font=FH, text_color=C["text"]).pack(pady=14, padx=20, anchor="w")

        self.body = ctk.CTkScrollableFrame(self, fg_color=C["bg"])
        self.body.pack(fill="both", expand=True, padx=20, pady=10)

        self.footer = ctk.CTkFrame(self, fg_color=C["surface"], height=56)
        self.footer.pack(fill="x", side="bottom")

    def field(self, label, var, placeholder=""):
        ctk.CTkLabel(self.body, text=label, font=FS, text_color=C["muted"]).pack(anchor="w", pady=(8, 2))
        e = ctk.CTkEntry(self.body, textvariable=var, placeholder_text=placeholder,
                         fg_color=C["surface2"], border_color=C["border"],
                         text_color=C["text"], font=FB, height=36)
        e.pack(fill="x")
        return e

    def dropdown(self, label, var, values):
        ctk.CTkLabel(self.body, text=label, font=FS, text_color=C["muted"]).pack(anchor="w", pady=(8, 2))
        ctk.CTkOptionMenu(self.body, variable=var, values=values,
                          fg_color=C["surface2"], button_color=C["border"],
                          button_hover_color=C["muted2"],
                          text_color=C["text"], font=FB).pack(fill="x")

    def textbox(self, label, height=80):
        ctk.CTkLabel(self.body, text=label, font=FS, text_color=C["muted"]).pack(anchor="w", pady=(8, 2))
        tb = ctk.CTkTextbox(self.body, height=height,
                            fg_color=C["surface2"], border_color=C["border"],
                            text_color=C["text"], font=FB)
        tb.pack(fill="x")
        return tb

    def buttons(self, ok_text="Guardar", ok_cmd=None, cancel_cmd=None):
        ctk.CTkButton(self.footer, text="Cancelar",
                       fg_color=C["surface2"], hover_color=C["surface"],
                       text_color=C["muted"], font=FB, width=100, height=34,
                       command=cancel_cmd or self.destroy).pack(side="right", padx=(4, 12), pady=11)
        ctk.CTkButton(self.footer, text=ok_text,
                       fg_color=C["accent3"], hover_color="#ea580c",
                       text_color="#fff", font=("Segoe UI", 12, "bold"),
                       width=120, height=34, command=ok_cmd).pack(side="right", padx=4, pady=11)


class StatCard(ctk.CTkFrame):
    def __init__(self, parent, label, value, color=None, **kw):
        super().__init__(parent, fg_color=C["surface"], corner_radius=10, **kw)
        accent = color or C["accent3"]
        top = ctk.CTkFrame(self, fg_color=accent, height=4, corner_radius=2)
        top.pack(fill="x", padx=0, pady=0)
        ctk.CTkLabel(self, text=str(value), font=("Segoe UI", 28, "bold"),
                     text_color=accent).pack(pady=(12, 2))
        ctk.CTkLabel(self, text=label, font=FS, text_color=C["muted"]).pack(pady=(0, 12))


# ═══════════════════════════════════════════════════════════════════════════
#  VISTA: RESUMEN DEL DÍA
# ═══════════════════════════════════════════════════════════════════════════

class ResumenView(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build()
        self.refresh()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))
        SectionHeader(top, "Resumen del Día",
                      f"Hoy: {date.today().strftime('%A %d de %B, %Y')}",
                      color=C["accent3"]).pack(side="left")
        ctk.CTkButton(top, text="↻  Actualizar",
                       fg_color=C["surface2"], hover_color=C["border"],
                       text_color=C["muted"], font=FB,
                       command=self.refresh, height=32).pack(side="right")

        # Tarjetas de estadísticas
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=(0, 16))
        self.cards_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.card_desayuno = StatCard(self.cards_frame, "Desayunos hoy", "—", C["accent3"])
        self.card_desayuno.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        self.card_comida = StatCard(self.cards_frame, "Comidas hoy", "—", C["accent2"])
        self.card_comida.grid(row=0, column=1, padx=4, sticky="nsew")
        self.card_cena = StatCard(self.cards_frame, "Cenas hoy", "—", C["accent4"])
        self.card_cena.grid(row=0, column=2, padx=4, sticky="nsew")
        self.card_total = StatCard(self.cards_frame, "Total servicios", "—", C["accent"])
        self.card_total.grid(row=0, column=3, padx=(8, 0), sticky="nsew")

        # Últimas asistencias
        ctk.CTkLabel(self, text="ÚLTIMAS ASISTENCIAS REGISTRADAS", font=FM,
                     text_color=C["muted2"]).pack(anchor="w", pady=(0, 6))

        cols = [
            ("id",       "ID",      50),
            ("alumno",   "Alumno",  200),
            ("tipo",     "Servicio",100),
            ("fecha",    "Fecha",   110),
            ("monto",    "Monto",    90),
            ("adeudo",   "Adeudo",   90),
        ]
        self.table = DataTable(self, cols)
        self.table.pack(fill="both", expand=True)

    def refresh(self):
        data = api("GET", f"/comedor/admin/asistencias/?fecha={date.today()}") or {}
        items = data.get("results", data) if isinstance(data, (dict, list)) else []
        if isinstance(items, dict):
            items = []

        # Contar por tipo
        conteo = {"desayuno": 0, "comida": 0, "cena": 0}
        for a in items:
            t = a.get("tipo_comida", "").lower()
            if t in conteo:
                conteo[t] += 1

        self.card_desayuno.pack_slaves()[1].configure(text=str(conteo["desayuno"]))
        self.card_comida.pack_slaves()[1].configure(text=str(conteo["comida"]))
        self.card_cena.pack_slaves()[1].configure(text=str(conteo["cena"]))
        self.card_total.pack_slaves()[1].configure(text=str(sum(conteo.values())))

        self.table.clear()
        for a in items[:50]:
            self.table.insert((
                a.get("id", ""),
                a.get("estudiante_nombre", a.get("estudiante", "")),
                a.get("tipo_comida", "").capitalize(),
                a.get("fecha_asistencia", ""),
                f"${a.get('precio', 0):.2f}",
                f"#{a.get('adeudo', '—')}",
            ))


# ═══════════════════════════════════════════════════════════════════════════
#  VISTA: REGISTRO DE ASISTENCIAS
# ═══════════════════════════════════════════════════════════════════════════

class AsistenciasView(ctk.CTkFrame):
    COLS = [
        ("id",      "ID",       50),
        ("alumno",  "Alumno",  210),
        ("tipo",    "Servicio",110),
        ("fecha",   "Fecha",   110),
        ("monto",   "Monto",    90),
        ("adeudo",  "Adeudo",   90),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._sel = None
        self._all = []
        self._build()
        self.refresh()

    def _build(self):
        # ── Barra superior
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        SectionHeader(top, "Registro de Asistencias",
                      "Control de consumos en cafetería",
                      color=C["accent3"]).pack(side="left")
        ctk.CTkButton(top, text="＋  Registrar asistencia",
                       fg_color=C["accent3"], hover_color="#ea580c",
                       text_color="#fff", font=("Segoe UI", 12, "bold"),
                       command=self.modal_registrar, height=36).pack(side="right")

        # ── Filtros de fecha y tipo
        filt = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=8)
        filt.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(filt, text="Fecha:", font=FS, text_color=C["muted"]).pack(side="left", padx=(12, 4), pady=10)
        self._fecha_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ctk.CTkEntry(filt, textvariable=self._fecha_var, width=120,
                     fg_color=C["surface2"], border_color=C["border"],
                     text_color=C["text"], font=FB, height=32).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(filt, text="Tipo:", font=FS, text_color=C["muted"]).pack(side="left", padx=(0, 4))
        self._tipo_var = tk.StringVar(value="todos")
        for val, lbl in [("todos", "Todos"), ("desayuno", "Desayuno"),
                          ("comida", "Comida"), ("cena", "Cena")]:
            ctk.CTkRadioButton(filt, text=lbl, variable=self._tipo_var, value=val,
                                fg_color=C["accent3"], text_color=C["muted"],
                                font=FS, command=self._apply_filters).pack(side="left", padx=8, pady=8)

        ctk.CTkButton(filt, text="Buscar",
                       fg_color=C["surface2"], hover_color=C["border"],
                       text_color=C["muted"], font=FS, height=30, width=80,
                       command=self.refresh).pack(side="right", padx=12, pady=8)

        # ── Tabla
        self.table = DataTable(self, self.COLS, on_select=self._on_sel)
        self.table.pack(fill="both", expand=True)

        # ── Botones
        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(fill="x", pady=(10, 0))
        self.btn_del = ctk.CTkButton(bf, text="🗑  Eliminar asistencia",
                                      fg_color=C["surface2"], hover_color="#3b0d0d",
                                      text_color=C["danger"], font=FB,
                                      state="disabled", command=self.eliminar, height=34)
        self.btn_del.pack(side="left")

    def _on_sel(self, vals):
        self._sel = vals
        self.btn_del.configure(state="normal" if vals else "disabled")

    def refresh(self):
        self.table.clear()
        fecha = self._fecha_var.get()
        path = f"/comedor/admin/asistencias/?fecha={fecha}"
        data = api("GET", path) or {}
        items = data.get("results", data) if isinstance(data, dict) else (data or [])
        self._all = items if isinstance(items, list) else []
        self._apply_filters()

    def _apply_filters(self):
        self.table.clear()
        tipo = self._tipo_var.get() if hasattr(self, "_tipo_var") else "todos"
        for a in self._all:
            if tipo != "todos" and a.get("tipo_comida", "").lower() != tipo:
                continue
            self.table.insert((
                a.get("id", ""),
                a.get("estudiante_nombre", a.get("estudiante", "")),
                a.get("tipo_comida", "").capitalize(),
                a.get("fecha_asistencia", ""),
                f"${a.get('precio', 0):.2f}",
                f"#{a.get('adeudo', '—')}",
            ))

    def modal_registrar(self):
        m = Modal(self, "Registrar Asistencia", h=440)
        v_est  = tk.StringVar()
        v_tipo = tk.StringVar(value="Desayuno")
        v_fec  = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))

        m.field("Matrícula o ID del estudiante *", v_est, "Ej: 1001")
        m.dropdown("Tipo de servicio *", v_tipo, ["Desayuno", "Comida", "Cena"])
        m.field("Fecha (YYYY-MM-DD)", v_fec)

        # Nota informativa
        ctk.CTkLabel(m.body,
                     text="ℹ  El adeudo se genera automáticamente.\n"
                          "   Se aplican descuentos por estrato/beca si están configurados.",
                     font=FS, text_color=C["muted"], justify="left",
                     wraplength=440).pack(anchor="w", pady=(10, 0))

        def guardar():
            if not v_est.get():
                messagebox.showwarning("Campo requerido", "Ingresa la matrícula del estudiante.", parent=m)
                return
            body = {
                "estudiante": v_est.get(),
                "tipo_comida": v_tipo.get().lower(),
                "fecha_asistencia": v_fec.get(),
            }
            r = api("POST", "/comedor/admin/asistencias/", body)
            if r and "id" in r:
                messagebox.showinfo("Registrado",
                                    f"Asistencia #{r['id']} registrada.\n"
                                    f"Adeudo generado: #{r.get('adeudo', '—')}", parent=m)
                m.destroy()
                self.refresh()
            elif r:
                messagebox.showerror("Error", str(r), parent=m)

        m.buttons("Registrar", ok_cmd=guardar, cancel_cmd=m.destroy)

    def eliminar(self):
        if not self._sel:
            return
        aid = self._sel[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar asistencia #{aid}?\nEsto no cancela el adeudo generado."):
            r = api("DELETE", f"/comedor/admin/asistencias/{aid}/")
            if r is not None:
                self.refresh()
                self.btn_del.configure(state="disabled")


# ═══════════════════════════════════════════════════════════════════════════
#  VISTA: MENÚ SEMANAL
# ═══════════════════════════════════════════════════════════════════════════

class MenuView(ctk.CTkFrame):
    DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    COLS = [
        ("id",    "ID",      50),
        ("semana","Semana",  120),
        ("dia",   "Día",    100),
        ("tipo",  "Tipo",    100),
        ("desc",  "Descripción", 320),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._sel = None
        self._build()
        self.refresh()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        SectionHeader(top, "Menú Semanal",
                      "Programación de platillos por día",
                      color=C["accent4"]).pack(side="left")
        ctk.CTkButton(top, text="＋  Agregar menú",
                       fg_color=C["accent4"], hover_color="#7c3aed",
                       text_color="#fff", font=("Segoe UI", 12, "bold"),
                       command=self.modal_agregar, height=36).pack(side="right")

        self.table = DataTable(self, self.COLS, on_select=self._on_sel)
        self.table.pack(fill="both", expand=True)

        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(fill="x", pady=(10, 0))
        self.btn_edit = ctk.CTkButton(bf, text="✏  Editar",
                                       fg_color=C["surface2"], hover_color=C["border"],
                                       text_color=C["text"], font=FB,
                                       state="disabled", command=self.modal_editar, height=34)
        self.btn_edit.pack(side="left", padx=(0, 8))

    def _on_sel(self, vals):
        self._sel = vals
        self.btn_edit.configure(state="normal" if vals else "disabled")

    def refresh(self):
        self.table.clear()
        data = api("GET", "/comedor/admin/menus/") or {}
        items = data.get("results", data) if isinstance(data, dict) else (data or [])
        for m in (items if isinstance(items, list) else []):
            self.table.insert((
                m.get("id", ""),
                m.get("semana", ""),
                m.get("dia", ""),
                m.get("tipo_comida", "").capitalize(),
                m.get("descripcion", m.get("notas", "")),
            ))

    def _form(self, title, v_sem, v_dia, v_tipo, tb_desc, ok_cmd):
        m = Modal(self, title, h=500)
        m.field("Semana (YYYY-WXX o fecha inicio)", v_sem, "Ej: 2025-W22")
        m.dropdown("Día", v_dia, self.DIAS)
        m.dropdown("Tipo de servicio", v_tipo, ["Desayuno", "Comida", "Cena"])
        ctk.CTkLabel(m.body, text="Descripción del platillo *", font=FS,
                     text_color=C["muted"]).pack(anchor="w", pady=(8, 2))
        desc_tb = ctk.CTkTextbox(m.body, height=100,
                                  fg_color=C["surface2"], border_color=C["border"],
                                  text_color=C["text"], font=FB)
        desc_tb.pack(fill="x")
        if tb_desc:
            desc_tb.insert("0.0", tb_desc)
        m.buttons("Guardar", ok_cmd=lambda: ok_cmd(m, desc_tb), cancel_cmd=m.destroy)
        return m

    def modal_agregar(self):
        v_sem  = tk.StringVar()
        v_dia  = tk.StringVar(value="Lunes")
        v_tipo = tk.StringVar(value="Desayuno")

        def guardar(m, desc_tb):
            desc = desc_tb.get("0.0", "end").strip()
            if not v_sem.get() or not desc:
                messagebox.showwarning("Campos requeridos", "Semana y Descripción son obligatorios.", parent=m)
                return
            body = {
                "semana": v_sem.get(),
                "dia": v_dia.get(),
                "tipo_comida": v_tipo.get().lower(),
                "descripcion": desc,
            }
            r = api("POST", "/comedor/admin/menus/", body)
            if r and "id" in r:
                messagebox.showinfo("Menú guardado", "Menú registrado correctamente.", parent=m)
                m.destroy()
                self.refresh()
            elif r:
                messagebox.showerror("Error", str(r), parent=m)

        self._form("Agregar Menú", v_sem, v_dia, v_tipo, "", guardar)

    def modal_editar(self):
        if not self._sel:
            return
        mid = self._sel[0]
        v_sem  = tk.StringVar(value=self._sel[1])
        v_dia  = tk.StringVar(value=self._sel[2])
        v_tipo = tk.StringVar(value=self._sel[3])

        def guardar(m, desc_tb):
            desc = desc_tb.get("0.0", "end").strip()
            body = {
                "semana": v_sem.get(),
                "dia": v_dia.get(),
                "tipo_comida": v_tipo.get().lower(),
                "descripcion": desc,
            }
            r = api("PUT", f"/comedor/admin/menus/{mid}/", body)
            if r:
                messagebox.showinfo("Actualizado", "Menú actualizado.", parent=m)
                m.destroy()
                self.refresh()

        self._form("Editar Menú", v_sem, v_dia, v_tipo, self._sel[4], guardar)


# ═══════════════════════════════════════════════════════════════════════════
#  VISTA: MENÚ ALUMNO (portal estudiante)
# ═══════════════════════════════════════════════════════════════════════════

class MenuAlumnoView(ctk.CTkFrame):
    DIAS_ORDER = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    TIPOS_COLOR = {
        "desayuno": C["accent3"],
        "comida":   C["accent2"],
        "cena":     C["accent4"],
    }

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build()
        self.refresh()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))
        SectionHeader(top, "Menú de la Semana",
                      "Consulta lo que hay disponible en el comedor",
                      color=C["accent"]).pack(side="left")
        ctk.CTkButton(top, text="↻  Actualizar",
                       fg_color=C["surface2"], hover_color=C["border"],
                       text_color=C["muted"], font=FB,
                       command=self.refresh, height=32).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

    def refresh(self):
        # Limpiar cards
        for w in self.scroll.winfo_children():
            w.destroy()

        data = api("GET", "/comedor/menu/") or {}
        items = data.get("results", data) if isinstance(data, dict) else (data or [])
        if not isinstance(items, list):
            items = []

        if not items:
            ctk.CTkLabel(self.scroll,
                         text="📋  No hay menú registrado para esta semana.",
                         font=FB, text_color=C["muted"]).pack(pady=40)
            return

        # Agrupar por día
        por_dia = {}
        for item in items:
            dia = item.get("dia", "")
            por_dia.setdefault(dia, []).append(item)

        # Renderizar en cards por día
        for dia in self.DIAS_ORDER:
            if dia not in por_dia:
                continue
            day_frame = ctk.CTkFrame(self.scroll, fg_color=C["surface"], corner_radius=10)
            day_frame.pack(fill="x", pady=(0, 10))

            hdr = ctk.CTkFrame(day_frame, fg_color=C["surface2"], corner_radius=0)
            hdr.pack(fill="x")
            ctk.CTkLabel(hdr, text=dia, font=("Segoe UI", 13, "bold"),
                         text_color=C["text"]).pack(side="left", padx=16, pady=10)

            for item in por_dia[dia]:
                tipo = item.get("tipo_comida", "").lower()
                color = self.TIPOS_COLOR.get(tipo, C["muted2"])

                row = ctk.CTkFrame(day_frame, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=6)

                badge = ctk.CTkLabel(row, text=tipo.capitalize(),
                                      font=FM, text_color=color,
                                      fg_color=color + "22",
                                      corner_radius=4, padx=8, pady=2)
                badge.pack(side="left")
                ctk.CTkLabel(row,
                              text=item.get("descripcion", item.get("notas", "Sin descripción")),
                              font=FB, text_color=C["text"],
                              anchor="w", wraplength=540).pack(side="left", padx=(10, 0))


# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR BUTTON
# ═══════════════════════════════════════════════════════════════════════════

class SideBtn(ctk.CTkButton):
    def __init__(self, parent, text, icon, cmd, **kw):
        super().__init__(parent, text=f"  {icon}  {text}",
                         fg_color="transparent", hover_color=C["surface2"],
                         anchor="w", text_color=C["muted"],
                         font=("Segoe UI", 12), height=40,
                         corner_radius=6, command=cmd, **kw)

    def activate(self, on: bool):
        self.configure(
            fg_color=C["surface2"] if on else "transparent",
            text_color=C["text"] if on else C["muted"]
        )


# ═══════════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

class ComedorApp(ctk.CTk):
    VIEWS = [
        ("resumen",    "Resumen del día",   "🏠", ResumenView),
        ("asistencias","Asistencias",       "✅", AsistenciasView),
        ("menu_admin", "Menú semanal",      "🍽", MenuView),
        ("menu_alumno","Ver menú (alumno)", "👀", MenuAlumnoView),
    ]

    def __init__(self):
        super().__init__()
        self.title("Comedor · SIGI-CEJLG")
        self.geometry("1200x700")
        self.configure(fg_color=C["bg"])
        self.minsize(920, 580)
        self._active = None
        self._btns   = {}
        self._cache  = {}
        self._layout()
        self.switch("resumen")

    def _layout(self):
        # Sidebar
        sb = ctk.CTkFrame(self, fg_color=C["surface"], width=220, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Cabecera sidebar
        hdr = ctk.CTkFrame(sb, fg_color=C["surface2"], corner_radius=0, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="🍴  Comedor",
                     font=("Segoe UI", 14, "bold"),
                     text_color=C["text"]).pack(pady=18, padx=18, anchor="w")

        ctk.CTkLabel(sb, text="VISTAS", font=("Consolas", 9),
                     text_color=C["muted2"]).pack(anchor="w", padx=16, pady=(18, 4))

        for key, label, icon, _ in self.VIEWS:
            b = SideBtn(sb, label, icon, cmd=lambda k=key: self.switch(k))
            b.pack(fill="x", padx=8, pady=2)
            self._btns[key] = b

        ctk.CTkFrame(sb, fg_color=C["border"], height=1).pack(fill="x", padx=12, pady=12)

        # Indicador conexión
        self._conn = ctk.CTkLabel(sb, text="⚡ Conectando…",
                                   font=FS, text_color=C["warn"])
        self._conn.pack(anchor="w", padx=16)

        # Info costo configurado
        self._costo_lbl = ctk.CTkLabel(sb, text="",
                                        font=FS, text_color=C["muted"])
        self._costo_lbl.pack(anchor="w", padx=16, pady=(6, 0))

        threading.Thread(target=self._check_conn, daemon=True).start()

        # Content
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def _check_conn(self):
        r = api("GET", "/comedor/admin/asistencias/")
        if r is not None:
            self._conn.configure(text="🟢 Conectado", text_color=C["accent"])
        else:
            self._conn.configure(text="🔴 Sin conexión", text_color=C["danger"])

    def switch(self, key: str):
        if self._active:
            self._active.pack_forget()
        for k, b in self._btns.items():
            b.activate(k == key)
        if key not in self._cache:
            cls = next(c for k, _, _, c in self.VIEWS if k == key)
            self._cache[key] = cls(self.content)
        self._active = self._cache[key]
        self._active.pack(fill="both", expand=True)


# ═══════════════════════════════════════════════════════════════════════════
#  LOGIN
# ═══════════════════════════════════════════════════════════════════════════

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIGI · Acceso Comedor")
        self.geometry("420x500")
        self.configure(fg_color=C["bg"])
        self.resizable(False, False)
        self._build()

    def _build(self):
        card = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=12)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.87, relheight=0.84)

        ctk.CTkLabel(card, text="🍴", font=("Segoe UI", 42)).pack(pady=(32, 4))
        ctk.CTkLabel(card, text="Módulo de Comedor",
                     font=("Segoe UI", 16, "bold"), text_color=C["text"]).pack()
        ctk.CTkLabel(card, text="SIGI · CEJLG", font=FS, text_color=C["muted"]).pack(pady=(2, 24))

        self._email = tk.StringVar()
        self._pwd   = tk.StringVar()

        for lbl, var, show in [("Correo electrónico", self._email, ""),
                                ("Contraseña",        self._pwd,   "●")]:
            ctk.CTkLabel(card, text=lbl, font=FS, text_color=C["muted"],
                         anchor="w").pack(fill="x", padx=28, pady=(8, 2))
            ctk.CTkEntry(card, textvariable=var, show=show,
                         fg_color=C["surface2"], border_color=C["border"],
                         text_color=C["text"], font=FB, height=38).pack(fill="x", padx=28)

        self._msg = ctk.CTkLabel(card, text="", font=FS, text_color=C["danger"])
        self._msg.pack(pady=(10, 0))

        ctk.CTkButton(card, text="Iniciar sesión",
                       fg_color=C["accent3"], hover_color="#ea580c",
                       text_color="#fff", font=("Segoe UI", 13, "bold"),
                       command=self._login, height=40).pack(fill="x", padx=28, pady=(12, 0))

        ctk.CTkButton(card, text="Entrar en modo demo",
                       fg_color="transparent", hover_color=C["surface2"],
                       text_color=C["muted"], font=FS,
                       command=self._demo).pack(pady=(8, 0))

    def _login(self):
        if not self._email.get() or not self._pwd.get():
            self._msg.configure(text="Completa todos los campos.")
            return
        self._msg.configure(text="Verificando…", text_color=C["warn"])
        self.update()
        r = api("POST", "/token/", {"email": self._email.get(), "password": self._pwd.get()})
        if r and "access" in r:
            global TOKEN
            TOKEN = r["access"]
            self._open()
        elif r and r.get("mfa_required"):
            self._mfa(self._email.get())
        else:
            self._msg.configure(text="Credenciales incorrectas.", text_color=C["danger"])

    def _mfa(self, email):
        m = Modal(self, "Verificación MFA", h=300)
        v = tk.StringVar()
        m.field("Código de 6 dígitos enviado a tu correo", v, "XXXXXX")

        def verify():
            r = api("POST", "/users/mfa/verify/", {"email": email, "code": v.get()})
            if r and "access" in r:
                global TOKEN
                TOKEN = r["access"]
                m.destroy()
                self._open()
            else:
                messagebox.showerror("Incorrecto", "Código inválido o expirado.", parent=m)

        m.buttons("Verificar", ok_cmd=verify, cancel_cmd=m.destroy)

    def _demo(self):
        self._open()

    def _open(self):
        self.destroy()
        ComedorApp().mainloop()


# ═══════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    ComedorApp().mainloop()
