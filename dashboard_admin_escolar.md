# Documentación de API: Dashboard Administrador Escolar

Esta documentación detalla los endpoints disponibles para el rol de **Administrador Escolar**. El sistema filtra automáticamente todos los resultados por el **nivel educativo** del administrador autenticado.

---

## Autenticación
Todos los endpoints requieren el encabezado `Authorization: Bearer <JWT_TOKEN>`.

---

## Tabla de Contenidos
1. [Maestros](#maestros)
2. [Grupos](#grupos)
3. [Materias](#materias)
4. [Asignaciones](#asignaciones)
5. [Calificaciones y Autorizaciones](#calificaciones)

---

<a name="maestros"></a>
## 1. MAESTROS

### 1.1 Listar Maestros del Nivel
Muestra los maestros que pertenecen al mismo nivel educativo que el administrador.

- **URL:** `GET /academico/api/admin-escolar/maestros/`
- **Método:** `GET`
- **Permisos:** `IsAdministradorEscolar`
- **Query Params:**
  - `search`: Búsqueda por nombre, email, etc.
  - `page`: Paginación.

**Respuesta (200 OK):**
```json
{
    "status": "success",
    "data": {
        "count": 1,
        "results": [
            {
                "id": 1,
                "nombre_completo": "Juan Perez",
                "email": "maestro@school.com",
                "num_asignaciones": 2,
                "materias_imparte": ["Matemáticas"]
            }
        ]
    }
}
```

---

<a name="grupos"></a>
## 2. GRUPOS

### 2.1 Listar Grupos del Nivel
- **URL:** `GET /academico/api/admin-escolar/grupos/`
- **Método:** `GET`
- **Orden:** Ciclo (desc), Grado (asc), Nombre (asc).

---

<a name="materias"></a>
## 3. MATERIAS

### 3.1 Crear Materia
- **URL:** `POST /academico/api/admin-escolar/materias/`
- **Cuerpo:**
```json
{
    "nombre": "Física I",
    "clave": "FIS101",
    "grado_id": 1,
    "programa_educativo_id": 1,
    "creditos": 6.0,
    "orden": 5,
    "fecha_inicio": "2025-09-01"
}
```

---

<a name="asignaciones"></a>
## 4. ASIGNACIONES

### 4.1 Listar Materias Disponibles para Asignación
Lista materias que no tienen maestro en un grupo.
- **URL:** `GET /academico/api/admin-escolar/asignaciones/materias-disponibles/`
- **Query Params:** `grupo_id` (requerido).

### 4.2 Crear Asignación
- **URL:** `POST /academico/api/admin-escolar/asignaciones/`
- **Cuerpo:** `{"maestro_id": 1, "grupo_id": 2, "materia_id": 3, "ciclo_escolar_id": 1}`

---

<a name="calificaciones"></a>
## 5. CALIFICACIONES Y AUTORIZACIONES

### 5.1 Autorizar Cambio
- **URL:** `POST /academico/api/admin-escolar/calificaciones/{id}/autorizar-cambio/`
- **Propósito:** Permite que un maestro edite una calificación ya bloqueada.
