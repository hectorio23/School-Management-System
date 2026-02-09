# Documentación de API: Dashboard Maestro

Esta documentación detalla los endpoints disponibles para el rol de **Maestro**. El sistema restringe el acceso únicamente a los grupos y estudiantes asignados al maestro autenticado.

---

## Autenticación
Todos los endpoints requieren el encabezado `Authorization: Bearer <JWT_TOKEN>`.

---

## Tabla de Contenidos
1. [Mis Asignaciones](#asignaciones)
2. [Mis Estudiantes](#estudiantes)
3. [Captura de Calificaciones](#calificaciones)

---

<a name="asignaciones"></a>
## 1. MIS ASIGNACIONES

### 1.1 Listar Asignaciones Activas
Muestra las materias y grupos que el maestro tiene asignados en el ciclo escolar actual.

- **URL:** `GET /academico/api/maestro/asignaciones/`
- **Método:** `GET`
- **Permisos:** `IsMaestro`

---

<a name="estudiantes"></a>
## 2. MIS ESTUDIANTES

### 2.1 Listar Estudiantes por Asignación
Muestra la lista de estudiantes inscritos en los grupos donde imparte clase.

- **URL:** `GET /academico/api/maestro/estudiantes/`
- **Método:** `GET`

---

<a name="calificaciones"></a>
## 3. CAPTURA DE CALIFICACIONES

### 3.1 Capturar Calificación
- **URL:** `POST /academico/api/maestro/calificaciones/`
- **Método:** `POST`
- **Cuerpo:**
```json
{
    "estudiante_id": 1001,
    "asignacion_maestro": 1,
    "periodo_evaluacion": 2,
    "calificacion": 9.5
}
```
**Reglas:**
1. Solo se permite durante la ventana de captura (7 días antes del fin del periodo).
2. Se bloquea automáticamente tras el primer guardado (`puede_modificar` = false).

### 3.2 Solicitar Cambio
- **URL:** `POST /academico/api/maestro/calificaciones/{id}/solicitar-cambio/`
- **Propósito:** Notifica al administrador que se requiere corregir una calificación ya bloqueada.
