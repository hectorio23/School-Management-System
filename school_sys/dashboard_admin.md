# Documentación de Endpoints - Dashboard Admin

Este documento detalla los endpoints disponibles para el panel administrativo. Se excluyen los endpoints de reportes.

**Nota Genera:** Todos los endpoints requieren autenticación. Se debe incluir el header:
`Authorization: Bearer <access_token>` (Token de un usuario administrador/superuser).

---

## 1. Estudiantes (Admin)

Gestión completa de estudiantes.

### Listar Estudiantes
**URL:** `/api/admin/students/`
**Método:** `GET`

```bash
curl -s -X GET http://127.0.0.1:8000/api/admin/students/ \
     -H "Content-type: application/json" \
     -H "Authorization: Bearer <access_token>"
```

### Crear Estudiante
Crea un usuario y su perfil de estudiante simultáneamente.

**URL:** `/api/admin/students/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/students/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "user_data": {
             "username": "nuevo_ingreso",
             "email": "nuevo@school.com",
             "password": "Password123"
         },
         "nombre": "Ricardo",
         "apellido_paterno": "Montaner",
         "apellido_materno": "Lopez",
         "direccion": "Calle Falsa 123",
         "grupo_id": 1
     }'
```

### Detalle Estudiante
Obtiene información completa de un estudiante específico.

**URL:** `/api/admin/students/<matricula>/`
**Método:** `GET`

```bash
curl -s -X GET http://127.0.0.1:8000/api/admin/students/220548/ \
     -H "Content-type: application/json" \
     -H "Authorization: Bearer <access_token>"
```

### Baja de Estudiante
Procesa la baja de un estudiante y calcula sus adeudos pendientes.

**URL:** `/api/admin/students/<matricula>/baja/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/students/220548/baja/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "justificacion": "Falta de pago",
         "es_temporal": false,
         "fecha_baja": "2026-01-20"
     }'
```

---

## 2. Tutores (Admin)

### Crear y Vincular Tutor
Crea un registro de tutor y lo asigna a estudiantes existentes.

**URL:** `/api/admin/students/tutores/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/students/tutores/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "nombre": "Don Ramón",
         "apellido_paterno": "Valdés",
         "apellido_materno": "Castillo",
         "telefono": "555-888-999",
         "correo": "rondamon@vecindad.com",
         "estudiantes_ids": [220548, 220330],
         "parentesco": "Padre"
     }'
```

### Listar Tutores
**URL:** `/api/admin/students/tutores/`
**Método:** `GET`



<!-- ## 3. Estratos Socioeconómicos

Configuración de los niveles socioeconómicos y becas. -->

### Crear Estrato
**URL:** `/api/admin/estratos/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/estratos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "nombre": "F",
         "descripcion": "Beca Total",
         "porcentaje_descuento": 100.00,
         "color": "#888888",
         "ingreso_minimo": 0,
         "ingreso_maximo": 1000
     }'
```



<!-- NOTA, los siguientees endpoints siguen en desarrollo -->

<!-- ## 4. Evaluaciones Socioeconómicas -->

<!-- ### Aprobar/Rechazar Evaluación
Permite a la comisión validar la evaluación socioeconómica de un alumno.

**URL:** `/api/admin/evaluaciones/<id>/aprobar/`
**Método:** `PUT`

```bash
curl -s -X PUT http://127.0.0.1:8000/api/admin/evaluaciones/1/aprobar/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "aprobado": true,
         "comentarios_comision": "Documentación validada correcta.",
         "estrato_id": 2
     }'
``` -->



<!-- ## 5. Finanzas (Adeudos y Pagos)

### Generar Adeudos Mensuales
Genera los cargos de colegiatura para todos los alumnos activos del mes especificado.

**URL:** `/api/admin/adeudos/generar-mensual/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/generar-mensual/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "mes": "2026-03"
     }'
``` -->

<!-- ### Aplicar Recargos
Aplica recargos y penalizaciones a los adeudos vencidos según la configuración.

**URL:** `/api/admin/adeudos/aplicar-recargos/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/aplicar-recargos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{}'
``` -->

<!-- ### Exentar Recargo
Elimina un cargo extra (multa/recargo) específico de un adeudo.

**URL:** `/api/admin/adeudos/<id_adeudo>/exentar/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/5/exentar/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "justificacion": "Error bancario comprobado"
     }'
``` -->

### Registrar Pago Manual
Registra un pago realizado en caja o ventanilla.

**URL:** `/api/admin/pagos/`
**Método:** `POST`

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/pagos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "adeudo": 10,
         "monto": 2500.00,
         "metodo_pago": "Efectivo",
         "referencia": "Recibo 555",
         "recibido_por": "Caja 1"
     }'
```


<!-- 
## 6. Configuración del Sistema

### Actualizar Configuración de Pagos
Define los días de corte y porcentajes de recargo.

**URL:** `/api/admin/configuracion-pago/`
**Método:** `PUT`

```bash
curl -s -X PUT http://127.0.0.1:8000/api/admin/configuracion-pago/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "dia_fin_ordinario": 15,
         "porcentaje_recargo": 12.50
     }'
``` -->



<!-- ## 7. Comedor

### Subir Menú Semanal (PDF)
Sube el archivo PDF del menú para la semana especificada.

**URL:** `/api/admin/comedor/menus/`
**Método:** `POST`
**Header:** `Content-Type: multipart/form-data` (manejado auto por curl con -F)

```bash
curl -s -X POST http://127.0.0.1:8000/api/admin/comedor/menus/ \
     -H "Authorization: Bearer <access_token>" \
     -F "semana_inicio=2026-02-01" \
     -F "semana_fin=2026-02-05" \
     -F "descripcion=Menu Feb 1" \
     -F "archivo_pdf=@/path/to/menu.pdf"
``` -->
