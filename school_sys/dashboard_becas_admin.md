# Documentación de Endpoints - Dashboard Becas Admin

Este documento detalla los endpoints disponibles para el rol `becas_admin` en el School Management System (SMS).

**Base URL:** `http://127.0.0.1:8000/api/admin/`

## Autenticación

Todos los endpoints requieren autenticación JWT con un usuario que tenga el rol `becas_admin`.

**Headers:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Permisos del Rol

El rol `becas_admin` tiene acceso a:
- Información de estudiantes (solo lectura)
- Gestión completa de becas
- Gestión de estratos socioeconómicos
- Evaluaciones socioeconómicas
- Asignación/retiro de becas a estudiantes

**No tiene acceso a:**
- CRUD de estudiantes (crear, modificar, eliminar)
- Adeudos y pagos
- Comedor
- Admisiones
- Panel Django Admin

---

## 1. Estudiantes (Solo Lectura)

### 1.1 Listar Estudiantes
- **Método:** `GET`
- **URL:** `/api/admin/students/`
- **Descripción:** Lista paginada de estudiantes (60 por página)

### 1.2 Detalle Estudiante
- **Método:** `GET`
- **URL:** `/api/admin/students/<matricula>/`
- **Descripción:** Información completa del estudiante, incluyendo becas y estratos

---

## 2. Tutores (Solo Lectura)

### 2.1 Listar Tutores
- **Método:** `GET`
- **URL:** `/api/admin/students/tutores/`

### 2.2 Detalle Tutor
- **Método:** `GET`
- **URL:** `/api/admin/students/tutores/<id>/`

---

## 3. Estratos Socioeconómicos (CRUD)

### 3.1 Listar Estratos
- **Método:** `GET`
- **URL:** `/api/admin/estratos/`

### 3.2 Crear Estrato
- **Método:** `POST`
- **URL:** `/api/admin/estratos/`
- **Cuerpo:**
```json
{
    "nombre": "ESTRATO A",
    "porcentaje_descuento": 10.00,
    "color": "#FF5733"
}
```

### 3.3 Actualizar Estrato
- **Método:** `PUT`
- **URL:** `/api/admin/estratos/<id>/`

### 3.4 Desactivar Estrato
- **Método:** `DELETE`
- **URL:** `/api/admin/estratos/<id>/`

---

## 4. Becas (CRUD)

### 4.1 Listar Becas
- **Método:** `GET`
- **URL:** `/api/admin/becas/`

### 4.2 Crear Beca
- **Método:** `POST`
- **URL:** `/api/admin/becas/`
- **Cuerpo:**
```json
{
    "nombre": "BECA EXCELENCIA",
    "porcentaje": 50.00,
    "fecha_vencimiento": "2026-12-31"
}
```

### 4.3 Actualizar Beca
- **Método:** `PUT`
- **URL:** `/api/admin/becas/<id>/`

### 4.4 Eliminar Beca
- **Método:** `DELETE`
- **URL:** `/api/admin/becas/<id>/`

### 4.5 Verificar Vigencia de Becas
- **Método:** `POST`
- **URL:** `/api/admin/becas/verificar-vigencia/`
- **Descripción:** Marca como vencidas las becas cuya fecha expiró

---

## 5. Becas-Estudiantes (Asignaciones)

### 5.1 Listar Asignaciones
- **Método:** `GET`
- **URL:** `/api/admin/becas-estudiantes/`

### 5.2 Asignar Beca
- **Método:** `POST`
- **URL:** `/api/admin/becas-estudiantes/`
- **Cuerpo:**
```json
{
    "beca": 1,
    "estudiante": 220548,
    "activa": true
}
```

### 5.3 Actualizar Asignación
- **Método:** `PUT`
- **URL:** `/api/admin/becas-estudiantes/<id>/`

### 5.4 Eliminar Asignación
- **Método:** `DELETE`
- **URL:** `/api/admin/becas-estudiantes/<id>/`

### 5.5 Retirar Becas Masivo
- **Método:** `POST`
- **URL:** `/api/admin/becas-estudiantes/retirar-masivo/`
- **Cuerpo:**
```json
{
    "ids": [1, 2, 3],
    "motivo": "Fin de ciclo escolar"
}
```

### 5.6 Activar Becas Masivo
- **Método:** `POST`
- **URL:** `/api/admin/becas-estudiantes/activar-masivo/`
- **Cuerpo:**
```json
{
    "ids": [1, 2, 3]
}
```

---

## 6. Evaluaciones Socioeconómicas

### 6.1 Listar Evaluaciones
- **Método:** `GET`
- **URL:** `/api/admin/students/evaluaciones/`

### 6.2 Detalle Evaluación
- **Método:** `GET`
- **URL:** `/api/admin/students/evaluaciones/<id>/`

---

## Notas de Seguridad

1. **MFA Obligatorio:** Este rol requiere autenticación de dos factores.
2. **Sin acceso a Django Admin:** El panel `/admin/` está restringido solo para TI.
3. **Auditoría:** Todas las acciones quedan registradas en el sistema.
