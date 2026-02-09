# Documentación de Endpoints - Dashboard Estudiantes

Este documento detalla los endpoints disponibles para el dashboard de estudiantes.

## 1. Login (Obtener Credenciales)

Endpoint para obtener los tokens de acceso (JWT) necesarios para realizar peticiones autenticadas.

**URL:** `/api/token/`
**Método:** `POST`

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "student_0_1468@test.com", "password": "password123"}'
```

**Respuesta Exitosa (200 OK):**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 2. Información del Estudiante

Antes de cargar el documento HTML principal, se debe realizar esta petición para obtener toda la información del estudiante basándose en su token JWT.

**URL:** `/students/info/`
**Método:** `GET`
**Headers:** `Authorization: Bearer <access_token>`

```bash
curl -X GET http://127.0.0.1:8000/students/info/ \
     -H "Authorization: Bearer <access_token>"
```

**Respuesta Exitosa (200 OK):**
```json
{
    "matricula": 220550,
    "nombre": "Maria",
    "apellido_paterno": "Hernandez",
    "apellido_materno": "Sanchez",
    "direccion": "Calle 59 Col. Centro",
    "grupo": {
        "nombre": "IRIC",
        "generacion": "2022-2026",
        "grado": {
            "nombre": "10",
            "nivel": "Universidad"
        }
    },
    "estado_actual": {
        "nombre": "Activo",
        "descripcion": "Estudiante inscrito y activo",
        "es_estado_activo": true
    },
    "evaluacion_socioeconomica": {
        "ingreso_mensual": 27841.0,
        "tipo_vivienda": "Propia",
        "miembros_hogar": 2,
        "estrato_nombre": "A",
        "porcentaje_descuento": 10.0,
        "aprobado": true,
        "fecha_evaluacion": "2026-01-18T02:51:06.554171Z"
    },
    "tutores": [
        {
            "tutor_id": 3,
            "nombre": "ROBERTA",
            "apellido_paterno": "OLED",
            "apellido_materno": "JARAMILLO",
            "telefono": "449 294 34 48",
            "correo": "roberta@test.com",
            "parentesco": "Madre"
        },
        {
            "tutor_id": 4,
            "nombre": "JASSIEL",
            "apellido_paterno": "NU\u00d1EZ",
            "apellido_materno": "PEDROZA",
            "telefono": "34 894 73 84",
            "correo": "ohyeah@outlook.es",
            "parentesco": "Padre"
        }
    ],
    "adeudos": [
        {
            "concepto_nombre": "COLEGIATURA",
            "monto_total": "2520.00",
            "estatus": "pendiente",
            "fecha_vencimiento": "2025-01-10"
        }
    ],
    "balance_total": 2520.0
}
```

---

## 3. Actualizar Tutores

Permite actualizar la información de uno o varios tutores asociados al estudiante.

**URL:** `/students/tutores/`
**Método:** `PUT`
**Headers:** 
- `Authorization: Bearer <access_token>`
- `Content-Type: application/json`

**Nota:** Es obligatorio enviar el `tutor_id` para identificar qué registro actualizar.

```bash
curl -s -X PUT http://127.0.0.1:8000/students/tutores/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
         "tutores": [
             {
                 "tutor_id": 3, 
                 "nombre": "Roberta Actualizada",
                 "apellido_paterno": "Oled",
                 "apellido_materno": "Jaramillo",
                 "telefono": "+52 449 999 9999",
                 "correo": "roberta_new@test.com"
             }
         ]
     }'
```

**Respuesta Exitosa (200 OK):**
```json
{
    "message": "Todos los tutores proporcionados fueron actualizados correctamente.",
    "tutores": [
        {
            "id": 3,
            "nombre": "Roberta Actualizada",
            "apellido_paterno": "Oled",
            "apellido_materno": "Jaramillo",
            "telefono": "+52 449 999 9999",
            "correo": "roberta_new@test.com",
            "parentesco": "Madre",
            "activo": true
        }
    ]
}
```

---

## 4. Crear Estudio Socioeconómico

Permite registrar una nueva evaluación socioeconómica. El sistema calculará automáticamente el estrato sugerido.

**URL:** `/students/estudio-socioeconomico/`
**Método:** `POST`
**Headers:** `Authorization: Bearer <access_token>`

**Nota:** 
- `ingreso_mensual` es un valor numérico (decimal).
- `miembros_hogar` es un valor numérico (entero).
- Los archivos (`acta_nacimiento`, `curp`) pueden enviarse como `multipart/form-data` si el frontend lo soporta, o manejarse por separado según configuración.

```bash
curl -X POST http://127.0.0.1:8000/students/estudio-socioeconomico/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
         "ingreso_mensual": 8500.00,
         "tipo_vivienda": "Rentada",
         "miembros_hogar": 4
     }'
```

**Respuesta Exitosa (201 Created):**
```json
{
    "message": "Evaluación socioeconómica registrada correctamente.",
    "estrato_sugerido": "B",
    "NOTA": "El administrador tiene que validar el Estrato socioeconómico"
}
```

---

## 5. Historial de Pagos (Nuevo)

Permite al alumno consultar su estado de cuenta detallado, incluyendo adeudos pendientes y pagados.

**URL:** `/students/pagos/historial/`
**Método:** `GET`
**Headers:** `Authorization: Bearer <access_token>`

**Respuesta Exitosa (200 OK):**
```json
{
    "balance_total": 520.00,
    "adeudos": [
        {
            "id": 10,
            "concepto": {"nombre": "Colegiatura Enero", "monto_base": "5000.00"},
            "monto_total": "4500.00",
            "monto_pagado": "4500.00",
            "estatus": "pagado",
            "pagos": [
                {"monto": "4500.00", "fecha_pago": "2024-01-05 10:00:00", "metodo_pago": "Transferencia"}
            ]
        }
    ]
}
```

## 6. Simulador de Pagos (Nuevo)

Calcula el monto a pagar en una fecha futura, incluyendo recargos automáticos si aplica (10% + $125).

**URL:** `/students/pagos/simular/`
**Método:** `POST`
**Body:** `{ "adeudo_id": 10, "fecha_pago": "2024-02-15" }`

**Respuesta Exitosa (200 OK):**
```json
{
    "adeudo_id": 10,
    "fecha_simulada": "2024-02-15",
    "desglose": {
        "monto_base": 5000.00,
        "descuento": 500.00,
        "recargo_estimado": 575.00,
        "subtotal_antes_recargo": 4500.00
    },
    "total_a_pagar": 5075.00
}
```
