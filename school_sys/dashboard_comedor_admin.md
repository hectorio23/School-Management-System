# Documentación de Endpoints - Dashboard Comedor Admin

Este documento detalla los endpoints disponibles para el rol `comedor_admin` en el School Management System (SMS).

**Base URL:** `http://127.0.0.1:8000/api/comedor/admin/`

## Autenticación

Todos los endpoints requieren autenticación JWT con un usuario que tenga el rol `comedor_admin`.

**Headers:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Permisos del Rol

El rol `comedor_admin` tiene acceso a:
- ✅ Información de estudiantes (solo lectura)
- ✅ Registro de asistencias al comedor
- ✅ Gestión de menús
- ✅ Reportes de comedor (diario, semanal, mensual)
- ✅ Alertas de alergias

**No tiene acceso a:**
- ❌ CRUD de estudiantes (crear, modificar, eliminar)
- ❌ Becas y estratos
- ❌ Adeudos y pagos generales
- ❌ Admisiones
- ❌ Panel Django Admin

---

## 1. Estudiantes (Solo Lectura)

### 1.1 Listar Estudiantes
- **Método:** `GET`
- **URL:** `/api/admin/students/`

### 1.2 Detalle Estudiante
- **Método:** `GET`
- **URL:** `/api/admin/students/<matricula>/`

---

## 2. Asistencias

### 2.1 Listar Asistencias
- **Método:** `GET`
- **URL:** `/api/comedor/admin/asistencias/`
- **Parámetros opcionales:** `?fecha=YYYY-MM-DD`

### 2.2 Registrar Asistencia
- **Método:** `POST`
- **URL:** `/api/comedor/admin/asistencias/registrar/`
- **Cuerpo:**
```json
{
    "estudiante_id": 220548,
    "tipo_comida": "Comida"
}
```
- **Nota:** Genera automáticamente un adeudo de comedor.

### 2.3 Historial de Estudiante
- **Método:** `GET`
- **URL:** `/api/comedor/admin/estudiante/<matricula>/`

---

## 3. Reportes

### 3.1 Reporte Diario
- **Método:** `GET`
- **URL:** `/api/comedor/admin/reportes/diario/?fecha=YYYY-MM-DD`

### 3.2 Reporte Semanal
- **Método:** `GET`
- **URL:** `/api/comedor/admin/reportes/semanal/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD`

### 3.3 Reporte Mensual
- **Método:** `GET`
- **URL:** `/api/comedor/admin/reportes/mensual/?mes=MM&anio=YYYY`

---

## 4. Alertas

### 4.1 Estudiantes con Alergias
- **Método:** `GET`
- **URL:** `/api/comedor/admin/alergias/`
- **Descripción:** Lista estudiantes con alergias alimentarias registradas para precaución en el comedor.

---

## 5. Menús

### 5.1 Listar Menús
- **Método:** `GET`
- **URL:** `/api/comedor/admin/menus/`

### 5.2 Crear Menú
- **Método:** `POST`
- **URL:** `/api/comedor/admin/menus/`
- **Cuerpo:**
```json
{
    "nombre": "Menú del Día",
    "descripcion": "Pollo con arroz",
    "precio": 50.00
}
```

### 5.3 Menú Semanal
- **Método:** `GET`
- **URL:** `/api/comedor/admin/menu-semanal/`

### 5.4 Crear Menú Semanal
- **Método:** `POST`
- **URL:** `/api/comedor/admin/menu-semanal/`

---

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `COMEDOR_DEFAULT_AMOUNT` | 10 | Costo por defecto del consumo |
| `APPLY_TOTAL_DISCOUNT` | 0 | 1=Aplicar descuentos, 0=No aplicar |
| `DIAS_VIGENCIA_ADEUDO_COMEDOR` | 10 | Días para vencimiento |
| `RECARGO_COMEDOR_PORCENTAJE` | 120 | Porcentaje de recargo (120 = 20%) |

---

## Notas de Seguridad

1. **MFA Obligatorio:** Este rol requiere autenticación de dos factores.
2. **Sin acceso a Django Admin:** El panel `/admin/` está restringido solo para TI.
3. **Auditoría:** Todas las acciones quedan registradas en el sistema.
