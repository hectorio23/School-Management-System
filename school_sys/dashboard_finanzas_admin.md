# Documentación de Endpoints - Dashboard Finanzas Admin

Este documento detalla los endpoints disponibles para el rol `finanzas_admin` en el School Management System (SMS).

**Base URL:** `http://127.0.0.1:8000/api/admin/`

## Autenticación

Todos los endpoints requieren autenticación JWT con un usuario que tenga el rol `finanzas_admin`.

**Headers:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Permisos del Rol

El rol `finanzas_admin` tiene acceso a:
- Información de estudiantes (solo lectura)
- Gestión completa de conceptos de pago
- Gestión de adeudos
- Gestión de pagos
- Reportes financieros

**No tiene acceso a:**
- CRUD de estudiantes (crear, modificar, eliminar)
- Becas y estratos
- Comedor
- Admisiones
- Panel Django Admin

---

## 1. Estudiantes (Solo Lectura)

### 1.1 Listar Estudiantes
- **Método:** `GET`
- **URL:** `/api/admin/students/`

### 1.2 Detalle Estudiante
- **Método:** `GET`
- **URL:** `/api/admin/students/<matricula>/`

---

## 2. Conceptos de Pago (CRUD)

### 2.1 Listar Conceptos
- **Método:** `GET`
- **URL:** `/api/admin/conceptos/`

### 2.2 Crear Concepto
- **Método:** `POST`
- **URL:** `/api/admin/conceptos/`
- **Cuerpo:**
```json
{
    "nombre": "COLEGIATURA ENERO",
    "descripcion": "MENSUALIDAD",
    "monto_base": 1500.00,
    "activo": true,
    "nivel_educativo": "PRIMARIA"
}
```

### 2.3 Actualizar Concepto
- **Método:** `PUT`
- **URL:** `/api/admin/conceptos/<id>/`

### 2.4 Eliminar Concepto
- **Método:** `DELETE`
- **URL:** `/api/admin/conceptos/<id>/`

### 2.5 Generar Adeudos Masivos
- **Método:** `POST`
- **URL:** `/api/admin/conceptos/<id>/generar-adeudos/`
- **Cuerpo:**
```json
{
    "aplicar_a_nivel": "PRIMARIA",
    "aplicar_a_grado": 1,
    "aplicar_a_grupo": null,
    "aplicar_a_estrato": null,
    "aplicar_a_matricula": ""
}
```

---

## 3. Adeudos (CRUD)

### 3.1 Listar Adeudos
- **Método:** `GET`
- **URL:** `/api/admin/pagos/adeudos/`

### 3.2 Crear Adeudo
- **Método:** `POST`
- **URL:** `/api/admin/pagos/adeudos/`
- **Cuerpo:**
```json
{
    "estudiante_matricula": 220548,
    "concepto_id": 1
}
```

### 3.3 Detalle Adeudo
- **Método:** `GET`
- **URL:** `/api/admin/pagos/adeudos/<id>/`

### 3.4 Actualizar Adeudo
- **Método:** `PUT`
- **URL:** `/api/admin/pagos/adeudos/<id>/`

### 3.5 Eliminar Adeudo
- **Método:** `DELETE`
- **URL:** `/api/admin/pagos/adeudos/<id>/`

### 3.6 Listar Adeudos Vencidos
- **Método:** `GET`
- **URL:** `/api/admin/pagos/adeudos/vencidos/`

### 3.7 Recalcular Recargos
- **Método:** `POST`
- **URL:** `/api/admin/pagos/adeudos/recalcular/`
- **Cuerpo (opcional):**
```json
{
    "ids": [1, 2, 3]
}
```
*Si se envía vacío, recalcula todos los adeudos pendientes.*

### 3.8 Exentar Recargo
- **Método:** `POST`
- **URL:** `/api/admin/pagos/adeudos/<id>/exentar/`
- **Cuerpo:**
```json
{
    "justificacion": "Pago pendiente por falla técnica"
}
```

---

## 4. Pagos

### 4.1 Listar Pagos
- **Método:** `GET`
- **URL:** `/api/admin/pagos/`

### 4.2 Crear Pago
- **Método:** `POST`
- **URL:** `/api/admin/pagos/`
- **Cuerpo:**
```json
{
    "adeudo": 1,
    "monto": 1500.00,
    "metodo_pago": "TRANSFERENCIA",
    "numero_referencia": "REF12345"
}
```

### 4.3 Detalle Pago
- **Método:** `GET`
- **URL:** `/api/admin/pagos/<id>/`

### 4.4 Actualizar Pago
- **Método:** `PUT`
- **URL:** `/api/admin/pagos/<id>/`

### 4.5 Eliminar Pago
- **Método:** `DELETE`
- **URL:** `/api/admin/pagos/<id>/`
- **Nota:** **BLOQUEADO** - No se permite eliminar pagos por integridad contable.

---

## 5. Reportes Financieros

### 5.1 Ingresos por Estrato
- **Método:** `GET`
- **URL:** `/api/admin/reportes/financieros/ingresos-estrato/?mes=MM&anio=YYYY`

### 5.2 Recaudación vs Recargos
- **Método:** `GET`
- **URL:** `/api/admin/reportes/financieros/recaudacion/?mes=MM&anio=YYYY`

### 5.3 Adeudos Vencidos
- **Método:** `GET`
- **URL:** `/api/admin/reportes/financieros/adeudos-vencidos/`

---

## Notas de Seguridad

1. **MFA Obligatorio:** Este rol requiere autenticación de dos factores.
2. **Sin acceso a Django Admin:** El panel `/admin/` está restringido solo para TI.
3. **Auditoría:** Todas las acciones quedan registradas en el sistema.
4. **Integridad Contable:** Los pagos no pueden ser eliminados, solo modificados.
