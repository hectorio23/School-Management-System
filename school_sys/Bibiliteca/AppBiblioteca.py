import customtkinter as ctk
from tkinter import messagebox
from conexion import obtener_conexion
from diseño import DashboardUI

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca")
        self.geometry("1100x650")

        self.ui = DashboardUI(self)
        self.ui.pack(fill="both", expand=True)

        self.db = obtener_conexion()
        if self.db:
            self.cursor = self.db.cursor(dictionary=True)

            self.ui.btn_inventario.configure(command=self.mostrar_inventario)
            self.ui.btn_prestamos.configure(command=self.mostrar_prestamos)
            self.ui.btn_admin.configure(command=self.administrar_biblioteca)

            self.ui.entry_busqueda.bind("<KeyRelease>", lambda e: self.mostrar_inventario())
            self.mostrar_inventario()

    # ---------------- INVENTARIO ----------------
    def mostrar_inventario(self):
        self.ui.preparar_tabla("Inventario de Libros")
        texto_busqueda = self.ui.entry_busqueda.get()

        if texto_busqueda:
            self.cursor.execute("SELECT * FROM Libros WHERE titulo LIKE %s", (f"%{texto_busqueda}%",))
        else:
            self.cursor.execute("SELECT * FROM Libros")

        for libro in self.cursor.fetchall():
            texto = f"{libro['isbn']} | {libro['titulo']} | Stock: {libro['cantidad']}"
            ctk.CTkLabel(self.ui.tabla_scroll, text=texto).pack(fill="x", padx=10, pady=5)

    # ---------------- PRESTAMOS ----------------
    def mostrar_prestamos(self):
        self.ui.preparar_tabla("Usuarios con Préstamos")

        ctk.CTkButton(self.ui.tabla_scroll, text="➕ Nuevo préstamo",
                      command=self.ventana_prestamo).pack(pady=10)

        query = """
            SELECT p.id_prestamo, u.nombre, l.titulo, p.fecha_salida, p.fecha_devolucion, l.id_libro
            FROM Prestamos p
            INNER JOIN Usuarios u ON p.id_usuario = u.id_usuario
            INNER JOIN Libros l ON p.id_libro = l.id_libro
        """
        self.cursor.execute(query)

        for p in self.cursor.fetchall():

            frame = ctk.CTkFrame(self.ui.tabla_scroll)
            frame.pack(fill="x", padx=10, pady=5)

            fecha = p['fecha_salida'].strftime("%Y-%m-%d")
            texto = f"{p['nombre']} --> {p['titulo']} ({fecha})"
            ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10)

            if not p['fecha_devolucion']:
                ctk.CTkButton(
                    frame,
                    text="Devolver",
                    command=lambda idp=p['id_prestamo'], idl=p['id_libro']:
                    self.devolver_libro(idp, idl)
                ).pack(side="right", padx=5)

    def devolver_libro(self, id_prestamo, id_libro):

        self.cursor.execute(
            "UPDATE Prestamos SET fecha_devolucion=CURDATE() WHERE id_prestamo=%s",
            (id_prestamo,)
        )

        self.cursor.execute(
            "UPDATE Libros SET cantidad=cantidad+1 WHERE id_libro=%s",
            (id_libro,)
        )

        self.db.commit()
        self.mostrar_prestamos()

    # ---------------- NUEVO PRESTAMO ----------------
    def ventana_prestamo(self):
        win = ctk.CTkToplevel(self)
        win.title("Nuevo préstamo")

        nombre = ctk.CTkEntry(win, placeholder_text="Nombre del usuario")
        nombre.pack(pady=5)

        self.cursor.execute("SELECT id_libro,titulo FROM Libros WHERE cantidad>0")
        libros = self.cursor.fetchall()
        valores = [l['titulo'] for l in libros]

        combo = ctk.CTkComboBox(win, values=valores)
        combo.pack(pady=5)

        def guardar():
            nombre_usuario = nombre.get()
            libro_titulo = combo.get()

            self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE nombre=%s", (nombre_usuario,))
            usuario = self.cursor.fetchone()

            if not usuario:
                self.cursor.execute("INSERT INTO Usuarios(nombre) VALUES(%s)", (nombre_usuario,))
                self.db.commit()
                id_usuario = self.cursor.lastrowid
            else:
                id_usuario = usuario['id_usuario']

            for l in libros:
                if l['titulo'] == libro_titulo:
                    id_libro = l['id_libro']

            self.cursor.execute(
                "INSERT INTO Prestamos(id_libro,id_usuario) VALUES(%s,%s)",
                (id_libro, id_usuario)
            )

            self.cursor.execute(
                "UPDATE Libros SET cantidad=cantidad-1 WHERE id_libro=%s",
                (id_libro,)
            )

            self.db.commit()
            win.destroy()
            self.mostrar_prestamos()

        ctk.CTkButton(win, text="Registrar préstamo", command=guardar).pack(pady=10)

    # ---------------- ADMIN LIBROS ----------------
    def administrar_biblioteca(self):
        self.ui.preparar_tabla("Administrar Biblioteca")

        ctk.CTkButton(self.ui.tabla_scroll, text="➕ Agregar Libro",
                      command=self.ventana_agregar).pack(pady=10)

        self.cursor.execute("SELECT * FROM Libros")
        for libro in self.cursor.fetchall():

            frame = ctk.CTkFrame(self.ui.tabla_scroll)
            frame.pack(fill="x", padx=10, pady=5)

            texto = f"{libro['titulo']} | {libro['autor']} | Stock: {libro['cantidad']}"
            ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10)

            ctk.CTkButton(frame, text="Editar",
                command=lambda l=libro: self.ventana_editar(l)).pack(side="right", padx=5)

            ctk.CTkButton(frame, text="Eliminar",
                command=lambda id=libro['id_libro']: self.eliminar_libro(id)).pack(side="right", padx=5)

    def ventana_agregar(self):
        win = ctk.CTkToplevel(self)
        win.title("Agregar libro")

        titulo = ctk.CTkEntry(win, placeholder_text="Titulo")
        titulo.pack(pady=5)

        autor = ctk.CTkEntry(win, placeholder_text="Autor")
        autor.pack(pady=5)

        isbn = ctk.CTkEntry(win, placeholder_text="ISBN")
        isbn.pack(pady=5)

        cantidad = ctk.CTkEntry(win, placeholder_text="Cantidad")
        cantidad.pack(pady=5)

        def guardar():
            self.cursor.execute(
                "INSERT INTO Libros(titulo,autor,isbn,cantidad) VALUES(%s,%s,%s,%s)",
                (titulo.get(), autor.get(), isbn.get(), cantidad.get())
            )
            self.db.commit()
            win.destroy()
            self.administrar_biblioteca()

        ctk.CTkButton(win, text="Guardar", command=guardar).pack(pady=10)

    def ventana_editar(self, libro):
        win = ctk.CTkToplevel(self)
        win.title("Editar libro")

        titulo = ctk.CTkEntry(win)
        titulo.insert(0, libro['titulo'])
        titulo.pack(pady=5)

        autor = ctk.CTkEntry(win)
        autor.insert(0, libro['autor'])
        autor.pack(pady=5)

        cantidad = ctk.CTkEntry(win)
        cantidad.insert(0, libro['cantidad'])
        cantidad.pack(pady=5)

        def actualizar():
            self.cursor.execute(
                "UPDATE Libros SET titulo=%s,autor=%s,cantidad=%s WHERE id_libro=%s",
                (titulo.get(), autor.get(), cantidad.get(), libro['id_libro'])
            )
            self.db.commit()
            win.destroy()
            self.administrar_biblioteca()

        ctk.CTkButton(win, text="Actualizar", command=actualizar).pack(pady=10)

    def eliminar_libro(self, id_libro):
        if messagebox.askyesno("Confirmar", "¿Eliminar libro?"):
            self.cursor.execute("DELETE FROM Libros WHERE id_libro=%s", (id_libro,))
            self.db.commit()
            self.administrar_biblioteca()


if __name__ == "__main__":
    app = App()
    app.mainloop()
