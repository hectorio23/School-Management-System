# Documentación de Endpoints - Dashboard Admisiones Admin

Este documento detalla los endpoints disponibles para el rol `admisiones_admin` en el School Management System (SMS).

**Base URL:** `http://127.0.0.1:8000/api/admission/`

## Autenticación

Todos los endpoints requieren autenticación JWT con un usuario que tenga el rol `admisiones_admin`.

**Headers:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Permisos del Rol

El rol `admisiones_admin` tiene acceso a:
- Gestión de aspirantes
- Visualización de documentos de aspirantes
- Migración de aspirantes a estudiantes
- Administración del proceso de admisión

**No tiene acceso a:**
- Información de estudiantes actuales
- Becas y estratos
- Adeudos y pagos
- Comedor
- Panel Django Admin

---

## 1. Documentos de Aspirantes

### 1.1 Ver Documento de Aspirante
- **Método:** `GET`
- **URL:** `/api/admission/admin/document/<folio>/<field_name>/`
- **Campos permitidos:**
  - `curp_pdf`
  - `acta_nacimiento`
  - `foto_credencial`
  - `boleta_ciclo_anterior`
  - `boleta_ciclo_actual`
- **Descripción:** Desencripta y muestra el documento del aspirante.

### 1.2 Ver Documento Específico de Aspirante
- **Método:** `GET`
- **URL:** `/api/admission/admin/aspirante/<folio>/<field_name>/`

### 1.3 Ver Documento de Tutor
- **Método:** `GET`
- **URL:** `/api/admission/admin/tutor/<tutor_id>/<field_name>/`
- **Campos permitidos:**
  - `acta_nacimiento`
  - `curp_pdf`
  - `comprobante_domicilio`
  - `foto_fachada_domicilio`
  - `comprobante_ingresos`
  - `carta_ingresos`
  - `ine_tutor`
  - `contrato_arrendamiento_predial`
  - `carta_bajo_protesta`

---

## 2. Migración de Aspirantes

### 2.1 Migrar Aspirante Individual
- **Método:** `POST`
- **URL:** `/api/admission/admin/<folio>/migrate/`
- **Descripción:** Convierte un aspirante ACEPTADO en estudiante activo.
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

### 2.2 Migrar Todos los Aceptados
- **Método:** `POST`
- **URL:** `/api/admission/admin/migrate-all/`
- **Cuerpo (opcional):**
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

## 3. Proceso de Admisión (Referencia)

El proceso de admisión sigue estas fases:

| Fase | Descripción |
|------|-------------|
| 1 | Solicitud de Preingreso |
| 2 | Análisis de Solicitudes |
| 3 | Visita Domiciliaria |
| 4 | Documentación Completa |
| 5 | Evaluación Pedagógica |
| 6 | Valoración por Comité |
| 7 | Publicación de Resultados |
| 8 | Aspirante Aceptado (listo para migrar) |

---

## 4. Plantillas Públicas

Estas plantillas están disponibles sin autenticación:

### 4.1 Descargar Carta de Ingresos
- **Método:** `GET`
- **URL:** `/api/admission/templates/carta_ingresos/`

### 4.2 Descargar Carta Bajo Protesta
- **Método:** `GET`
- **URL:** `/api/admission/templates/carta_bajo_protesta/`

---

## Notas de Seguridad

1. **MFA Obligatorio:** Este rol requiere autenticación de dos factores.
2. **Sin acceso a Django Admin:** El panel `/admin/` está restringido solo para TI.
3. **Documentos Encriptados:** Todos los documentos de aspirantes están encriptados en el servidor.
4. **Auditoría:** Todas las acciones de migración quedan registradas en el sistema.
