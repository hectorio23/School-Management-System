# Documentación de Endpoints - Dashboard Admin

Este documento detalla los endpoints disponibles para el panel administrativo remoto del School Management System (SMS).

**Base URL:** `http://127.0.0.1:8000/api/admin/`

## Autenticación y Tokens

TODOS los endpoints requieren el encabezado `Authorization`.

**Headers:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Nota:** Actualmente los permisos están en `AllowAny` para facilitar las pruebas iniciales, pero el flujo está diseñado para requerir un token JWT de un usuario con privilegios de administrador (`is_staff` o `is_superuser`).

---

## 1. Estudiantes (api/admin/students/)

### 1.1 Listar Estudiantes
Retorna una lista paginada (60 por página).
<!-- TODO: Cambiar a n > 300 en producción  -->
- **Método:** `GET`
- **URL:** `/api/admin/students/`
- **Respuesta (200 OK):**
```json
{
    "count": 120,
    "next": "http://.../api/admin/students/?page=2",
    "previous": null,
    "results": [
        {
            "matricula": 220548,
            "nombre_completo": "JUAN PÉREZ GARCÍA",
            "grupo_nombre": "A",
            "grado_nombre": "1°",
            "nivel_educativo": "PRIMARIA",
            "estatus": "ACTIVO"
        }
    ]
}
```

### 1.2 Crear Estudiante
Crea un usuario de Django y su perfil de estudiante asociado.
- **Método:** `POST`
- **URL:** `/api/admin/students/create/`
- **Cuerpo (JSON):**
```json
{
    "user_data": {
        "username": "ALUMNO2026",
        "email": "alumno@school.com",
        "password": "Password123"
    },
    "nombre": "JUAN",
    "apellido_paterno": "MADRAZO",
    "apellido_materno": "MADDEVDEV",
    "direccion": "YESIS MARIE",
    "telefono": "555-1234",
    "curp": "CURP1234567890",
    "grupo_id": 1
}
```
- **Respuesta (201 Created):** Datos del estudiante creado.

### 1.3 Detalle Estudiante
- **Método:** `GET`
- **URL:** `/api/admin/students/<matricula>/`
- **Respuesta (200 OK):** Detalle completo incluyendo información del usuario, grupo y estatus.

### 1.4 Actualizar Estudiante
- **Método:** `PUT`
- **URL:** `/api/admin/students/<matricula>/update/`
- **Cuerpo (JSON):** Campos a actualizar (parcial o total).
- **Respuesta (200 OK):** Objeto actualizado.

### 1.5 Baja de Estudiante (Soft Delete)
Cambia el estado del estudiante a "BAJA" e inactiva su usuario.
- **Método:** `DELETE`
- **URL:** `/api/admin/students/<matricula>/update/`
- **Respuesta (204 No Content):** Sin cuerpo.

---

## 2. Tutores (api/admin/students/tutores/)

### 2.1 Listar Tutores
- **Método:** `GET`
- **URL:** `/api/admin/students/tutores/`
- **Respuesta (200 OK):** Lista paginada (150 por página).

### 2.2 Crear/Editar Tutor
- **Método:** `POST` (Crear) / `PUT` (Editar)
- **URL:** `/api/admin/students/tutores/` o `/api/admin/students/tutores/<id>/`
- **Cuerpo (JSON):**
```json
{
    "nombre": "MARÍA",
    "apellido_paterno": "LÓPEZ",
    "apellido_materno": "SÁNCHEZ",
    "telefono": "555-9876",
    "correo": "maria@email.com",
    "parentesco": "MADRE",
    "estudiantes_ids": [220548]
}
```

### 2.3 Eliminar Tutor
- **Método:** `DELETE`
- **URL:** `/api/admin/students/tutores/<id>/`

---

## 3. Conceptos de Pago (api/admin/conceptos/)

### 3.1 CRUD Básico
- **Métodos:** `GET`, `POST`, `PUT`, `DELETE`
- **URLs:** `/api/admin/conceptos/` o `/api/admin/conceptos/<id>/`
- **Cuerpo (POST/PUT):**
```json
{
    "nombre": "COLEGIATURA ENERO",
    "descripcion": "MENSUALIDAD",
    "monto_base": 1500.00,
    "activo": true,
    "nivel_educativo": "PRIMARIA"
}
```

### 3.2 Generar Adeudos Masivos
Lanza el proceso de creación de adeudos para estudiantes según filtros.
- **Método:** `POST`
- **URL:** `/api/admin/conceptos/<id>/generar-adeudos/`
- **Cuerpo (JSON):**
```json
{
    "aplicar_a_nivel": "PRIMARIA",
    "aplicar_a_grado": 1,
    "aplicar_a_grupo": null,
    "aplicar_a_estrato": null,
    "aplicar_a_matricula": ""
}
```
- **Respuesta (200 OK):** `{"message": "Generando adeudos para X estudiantes..."}`

---

## 4. Grados (api/admin/grados/)
- **CRUD:** `GET`, `POST`, `PUT`, `DELETE`
- **Cuerpo:** `{"nombre": "1°", "nivel": "PRIMARIA"}`

---

## 5. Grupos (api/admin/grupos/)
- **CRUD:** `GET`, `POST`, `PUT`, `DELETE`
- **Cuerpo:** `{"nombre": "A", "grado": 1, "generacion": "2025-2026"}`

---

## 6. Estratos Socioeconómicos (api/admin/estratos/)
- **CRUD:** `GET`, `POST`, `PUT`, `DELETE` (Delete desactiva).
- **Cuerpo:** 
```json
{
    "nombre": "ESTRATO A",
    "porcentaje_descuento": 10.00,
    "color": "#FF5733"
}
```

---

## 7. Estados de Estudiante (api/admin/estados/)
- **CRUD:** `GET`, `POST`, `PUT`, `DELETE`
- **Cuerpo:** `{"nombre": "ACTIVO", "es_estado_activo": true}`

---

## 8. Becas (api/admin/becas/)

### 8.1 CRUD Básico
- **Métodos:** `GET`, `POST`, `PUT`, `DELETE`
- **Cuerpo:**
```json
{
    "nombre": "BECA EXCELENCIA",
    "porcentaje": 50.00,
    "fecha_vencimiento": "2026-12-31"
}
```

### 8.2 Verificar Vigencia
Actualiza el estatus `valida` de todas las becas según la fecha actual.
- **Método:** `POST`
- **URL:** `/api/admin/becas/verificar-vigencia/`
- **Respuesta (200 OK):** Mensaje de éxito.

---

## 9. Becas-Estudiantes (api/admin/becas-estudiantes/)

### 9.1 CRUD Básico (Asignación Individual)
- **Métodos:** `GET`, `POST`, `PUT`, `DELETE`
- **Cuerpo (POST):** `{"beca": 1, "estudiante": 220548, "activa": true}`

### 9.2 Retirar Masivo
- **Método:** `POST`
- **URL:** `/api/admin/becas-estudiantes/retirar-masivo/`
- **Cuerpo:** `{"ids": [1, 2, 3], "motivo": "MAL COMPORTAMIENTO"}`

### 9.3 Activar Masivo
- **Método:** `POST`
- **URL:** `/api/admin/becas-estudiantes/activar-masivo/`
- **Cuerpo:** `{"ids": [1, 2, 3]}`

---

## 10. Adeudos (api/admin/pagos/adeudos/)

### 10.1 CRUD Básico
- **URLs:** `/api/admin/pagos/adeudos/` o `/api/admin/pagos/adeudos/<id>/`
- **Cuerpo (POST):** `{"estudiante_matricula": 220548, "concepto_id": 1}`

### 10.2 Listar Vencidos
- **Método:** `GET`
- **URL:** `/api/admin/pagos/adeudos/vencidos/`

### 10.3 Recalcular Recargos
- **Método:** `POST`
- **URL:** `/api/admin/pagos/adeudos/recalcular/`
- **Cuerpo (Opcional):** `{"ids": [1, 2, 3]}`. Si se envía vacío, se recalcula todo.

### 10.4 Exentar Recargo
- **Método:** `POST`
- **URL:** `/api/admin/pagos/adeudos/<id>/exentar/`
- **Cuerpo:** `{"justificacion": "PAGO PENDIENTE POR FALLA TÉCNICA"}`

---

## 11. Pagos (api/admin/pagos/)

### 11.1 Listar/Crear/Detalle/Update
- **URLs:** `/api/admin/pagos/` o `/api/admin/pagos/<id>/`
- **Cuerpo (POST):**
```json
{
    "adeudo": 1,
    "monto": 1500.00,
    "metodo_pago": "TRANSFERENCIA",
    "numero_referencia": "REF12345"
}
```
- **DELETE:** **BLOQUEADO (403 Forbidden)**. No se permite eliminar pagos por integridad contable.

---

## 12. Evaluaciones (api/admin/students/evaluaciones/)

### 12.1 Listar/Detalle
- **Métodos:** `GET` solamente.
- **URLs:** `/api/admin/students/evaluaciones/` o `/api/admin/students/evaluaciones/<id>/`
- **Respuesta:** Detalle de estudios socioeconómicos realizados por los estudiantes.

---

## 13. Comedor (api/comedor/admin/)

### 13.1 Asistencias
- **Listar:** `GET /api/comedor/admin/asistencias/?fecha=YYYY-MM-DD`
- **Registrar:** `POST /api/comedor/admin/asistencias/registrar/`
  - Body: `{"estudiante_id": 1, "tipo_comida": "Comida"}`
  - *Genera automáticamente un adeudo de comedor.*

### 13.2 Reportes
- **Diario:** `GET /api/comedor/admin/reportes/diario/?fecha=YYYY-MM-DD`
- **Semanal:** `GET /api/comedor/admin/reportes/semanal/?fecha_inicio=...&fecha_fin=...`
- **Mensual:** `GET /api/comedor/admin/reportes/mensual/?mes=MM&anio=YYYY`

### 13.3 Alertas
- **Alergias:** `GET /api/comedor/admin/alergias/` (Lista estudiantes con alergias)

---

## 14. Reportes Financieros (api/admin/reportes/financieros/)

### 14.1 Ingresos por Estrato
- **URL:** `GET .../ingresos-estrato/?mes=MM&anio=YYYY`
- **Salida:** Desglose anual y mensual de ingresos por cada estrato socioeconómico.

### 14.2 Recaudación vs Recargos
- **URL:** `GET .../recaudacion/?mes=MM&anio=YYYY`
- **Salida:** Total recaudado y estimación de cuánto corresponde a deuda base vs recargos.

### 14.3 Adeudos Vencidos
- **URL:** `GET .../adeudos-vencidos/`
- **Salida:** Lista de estudiantes con deuda vencida y montos totales.

---

## 15. Reportes Académicos y Exportación (api/admin/)

### 15.1 Estadísticas
- **URL:** `GET /api/admin/reportes/academicos/estadisticas/`
- **Dato:** Inscritos activos, reinscripciones ciclo actual, bajas históricas.

### 15.2 Exportar Estudiantes
- **URL:** `GET /api/admin/exportar/estudiantes/?format=excel` (o `pdf`)
- **Descarga:** Archivo .xlsx o .pdf con listado completo.

### 15.3 Exportar Aspirantes
- **URL:** `GET /api/admin/exportar/aspirantes/`
- **Descarga:** Archivo .xlsx con listado de aspirantes en proceso.

---

## 16. Migración de Aspirantes (api/admission/admin/)

### 16.1 Migrar Aspirante Individual
Convierte un aspirante ACEPTADO en estudiante activo.
- **Método:** `POST`
- **URL:** `/api/admission/admin/<folio>/migrate/`
- **Validaciones:**
  - Status: ACEPTADO
  - Fase >= 4 (documentos completos)
  - Ciclo escolar activo (< 3 meses desde inicio)
  - Grupo disponible con cupo (máx. 30 estudiantes)
- **Respuesta (201 Created):**
```json
{
    "message": "Aspirante migrado exitosamente a estudiante",
    "estudiante": {
        "matricula": 220610,
        "nombre_completo": "JUAN PÉREZ GARCÍA",
        "grupo": "1°A Primaria",
        "email": "juan@school.com",
        "username": "juan"
    },
    "tutores_vinculados": [1, 2]
}
```

### 16.2 Migrar Todos los Aceptados
Migra en lote todos los aspirantes con status ACEPTADO.
- **Método:** `POST`
- **URL:** `/api/admission/admin/migrate-all/`
- **Cuerpo (JSON, opcional):**
```json
{
    "nivel_ingreso": "Primaria"
}
```
- **Respuesta (200 OK):**
```json
{
    "message": "Proceso de migración completado",
    "resumen": {
        "total_procesados": 25,
        "migrados_exitosamente": 23,
        "con_errores": 2
    },
    "detalle": {
        "migrados": [...],
        "errores": [...]
    }
}
```

---

## 17. Cronjobs (Tareas Programadas)

### 17.1 Generación de Reinscripción
**Archivo:** `cron_reinscripcion.py`
- **Frecuencia:** Una vez al inicio del ciclo escolar
- **Cron:** `0 0 1 8 *` (1 de agosto)
- **Acción:** 
  - Genera adeudo "Reinscripción [ciclo]" para estudiantes activos
  - Cambia status a "No Reinscrito"
- **Ejecución:**
```bash
python manage.py shell < cron_reinscripcion.py
```

### 17.2 Recálculo de Adeudos Vencidos
**Archivo:** `cron_adeudos_vencidos.py`
- **Frecuencia:** Diario a las 00:01
- **Cron:** `1 0 * * *`
- **Variables de entorno:**
  - `OVERDUE_FIXED_SURCHARGE`: Recargo fijo (default: $125)
  - `OVERDUE_DAILY_PERCENTAGE`: Porcentaje diario (default: 10%)
  - `DAYS_BEFORE_DEACTIVATION`: Días antes de baja (default: 10)
- **Acción:**
  - Aplica recargo fijo una sola vez
  - Aplica 10% diario después del primer día
  - Status -> "Vencido"
  - Después de N días: da de baja y congela adeudo
  - Envía emails a estudiante y tutores

### 17.3 Recordatorio de Estudio Socioeconómico
**Archivo:** `cron_recordatorio_socioeconomico.py`
- **Frecuencia:** Mensual (día 1)
- **Cron:** `0 9 1 * *`
- **Variables de entorno:**
  - `MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES`: Meses entre estudios (default: 1)
- **Acción:**
  - Verifica si el ciclo termina en < 2 meses
  - Identifica estudiantes sin estudio reciente
  - Envía recordatorio por email

---

## 18. Variables de Entorno de Producción

### 18.1 Comedor
| Variable | Default | Descripción |
|----------|---------|-------------|
| `COMEDOR_DEFAULT_AMOUNT` | 10 | Costo por defecto del consumo |
| `APPLY_TOTAL_DISCOUNT` | 0 | 1=Aplicar descuentos, 0=No aplicar |
| `DIAS_VIGENCIA_ADEUDO_COMEDOR` | 10 | Días para vencimiento |
| `RECARGO_COMEDOR_PORCENTAJE` | 120 | Porcentaje de recargo (120 = 20%) |

### 18.2 Adeudos
| Variable | Default | Descripción |
|----------|---------|-------------|
| `OVERDUE_FIXED_SURCHARGE` | 125 | Recargo fijo en pesos |
| `OVERDUE_DAILY_PERCENTAGE` | 10 | Porcentaje diario |
| `DAYS_BEFORE_DEACTIVATION` | 10 | Días antes de dar de baja |

### 18.3 Estudios Socioeconómicos
| Variable | Default | Descripción |
|----------|---------|-------------|
| `MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES` | 1 | Meses entre estudios |

---

## 19. Scripts de Testing

### 19.1 Ubicación
- `test_endpoints_admin.sh` - Endpoints administrativos
- `test_endpoints_estudiante.sh` - Endpoints de estudiantes
- `test_endpoints_admissions.sh` - Flujo de admisiones
- `test_endpoints_comedor.sh` - Endpoints de comedor

### 19.2 Uso
```bash
# Dar permisos de ejecución
chmod +x test_endpoints_*.sh

# Ejecutar con token
export TOKEN="eyJhbGciOiJIUzI1..."
./test_endpoints_admin.sh http://127.0.0.1:8000 "$TOKEN"

# O pasar como argumento
./test_endpoints_estudiante.sh http://127.0.0.1:8000
```
