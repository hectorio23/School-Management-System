# Documentación de API: Dashboard Biblioteca

Esta documentación detalla los endpoints disponibles para el rol de **Administrador de Biblioteca**. Este rol es el único autorizado para gestionar el catálogo, los préstamos y las multas.

---

## Autenticación
Todos los endpoints requieren el encabezado `Authorization: Bearer <JWT_TOKEN>`.
Se requiere el rol de usuario `bibliotecario`.

---

## Tabla de Contenidos
1. [Libros](#libros)
2. [Usuarios](#usuarios)
3. [Préstamos](#prestamos)
4. [Multas](#multas)

---

<a name="libros"></a>
## 1. LIBROS

### 1.1 Listar y Crear Libros
- **URL:** `GET /biblioteca/libros/` | `POST /biblioteca/libros/`
- **Permisos:** `IsBibliotecario`

**Cuerpo para Crear (POST):**
```json
{
    "titulo": "Cien Años de Soledad",
    "autor": "Gabriel García Márquez",
    "editorial": "Sudamericana",
    "anio": 1967,
    "genero": "Realismo Mágico",
    "isbn": "978-0307474728",
    "numero_de_ejemplares": 5
}
```

---

<a name="usuarios"></a>
## 2. USUARIOS DE BIBLIOTECA

### 2.1 Gestión de Usuarios
- **URL:** `GET /biblioteca/usuarios/` | `POST /biblioteca/usuarios/`
- **Nota:** Los usuarios deben estar previamente registrados en el sistema central de usuarios.

---

<a name="prestamos"></a>
## 3. PRÉSTAMOS

### 3.1 Realizar Préstamo
- **URL:** `POST /biblioteca/prestamos/realizar/`
- **Reglas de Negocio:** 
  1. El usuario no debe tener multas pendientes.
  2. El libro debe tener ejemplares disponibles.

**Cuerpo (POST):**
```json
{
    "libro": 1,
    "usuario": 5,
    "dias": 7
}
```

### 3.2 Devolver Libro
- **URL:** `POST /biblioteca/prestamos/{id}/devolver/`
- **Descripción:** Marca el préstamo como devuelto y libera el ejemplar en el stock.

---

<a name="multas"></a>
## 4. MULTAS

### 4.1 Listar Multas
- **URL:** `GET /biblioteca/multas/`
- **Query Params:** `?estado=pendiente` o `?estado=pagada`

### 4.2 Pagar Multa
- **URL:** `POST /biblioteca/multas/{id}/pagar/`
- **Descripción:** Registra el pago de una multa pendiente.

---

## Notificaciones Automáticas
El sistema cuenta con un proceso diario (Cronjob) que:
1. Detecta préstamos vencidos.
2. Genera automáticamente una multa de **$50.00**.
3. Envía un correo electrónico al usuario notificando el adeudo pendiente.
