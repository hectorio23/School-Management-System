#!/bin/bash
# Script para probar el endpoint de login con curl
## Por el momento no esta habilitado el JWT, pero esto sirve para probar que los endponts pueden
# recibir y repsonder correctamente.


## Retornará 200 OK -> pagina del index (login)
curl -X GET http://127.0.0.1:8000/ \
     -H "Content-Type: application/json"



# Retornará 2 tokens, el access_token y el refresh token
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "adancpphack@gmail.com", "password": "testpass123"}'


# Retorna la info para el dashboard del propio estudiante
curl -X GET http://127.0.0.1:8000/students/info/ \
      -H "Authorization: Bearer <token>"



# UPDATE TUTORES, PUEDE SER 1, 2, 3, ....
curl -s -X PUT http://127.0.0.1:8000/students/tutores/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "tutores": [
             {
                 "tutor_id": <tutor_id>,
                 "nombre": "Maria Actualizada",
                 "apellido_paterno": "Garcia",
                 "apellido_materno": "Lopez",
                 "telefono": "+52 449 888 8888",
                 "correo": "updated@ejemplo.com"
             }
         ]
     }'


#############################################################3
#####3############# ADMIN request ############################
#############################################################3

# Retornar El listado de unos cuantos estudiantes
curl -s -X GET http://127.0.0.1:8000/api/admin/students/ -H "Content-type: application/json" -H "Authorization: Bearer <access_Token>"
# retornará algo como esto (para el dashboard de admin) en caso de hacerle la peticion correctamente: 
# {
#   "count": 2,
#   "next": null,
#   "previous": null,
#   "results": [
#     {
#       "matricula": 220330,
#       "apellido_paterno": "PANDILLA",
#       "apellido_materno": "RIVERS",
#       "nombres": "MAURICER",
#       "grado": "10 Universidad",
#       "grupo": "DSGM",
#       "estrato": "Sin Asignar",
#       "estatus": "Sin Estado"
#     },
#     {
#       "matricula": 220548,
#       "apellido_paterno": "FLOWERS",
#       "apellido_materno": "KRAKOV",
#       "nombres": "MARIANA",
#       "grado": "10 Universidad",
#       "grupo": "IRIC",
#       "estrato": "B",
#       "estatus": "Activo"
#     }
#   ]
# }

# Retornar TODA la informacion de un estudiante en específico < FOR Admins ONLY>
curl -s -X GET http://127.0.0.1:8000/api/admin/students/220548/ -H "Content-type: application/json" -H "Authorization: Bearer <acess_token>"
# Retorna un objeto como el siguiente:
# {
#     "informacion_personal":{
#         "matricula":220548,
#         "nombre_completo":"MARIANA FLOWERS KRAKOV",
#         "nombres":"MARIANA",
#         "apellido_paterno":"FLOWERS",
#         "apellido_materno":"KRAKOV",
#         "curp":"adan",
#         "email":"adancpphack@gmail.com",
#         "direccion":"CHUY MARRY",
#         "grupo":"IRIC - 2022-2026",
#         "grado":"10 - Universidad"
#     },
#     "resumen_academico":{
#         "estrato_actual":"B",
#         "estado_escolar":"Activo",
#         "balance_adeudo":4000.0
#     },
#     "tutores":[
#         {
#             "id":1,
#             "nombre":"Maria Pereira Garcia Lopez",
#             "telefono":"+52 449 888 8888",
#             "correo":"updated@ejemplo.com",
#             "parentesco":"Madre","activo":true
#         },
#         {
#             "id":2,
#             "nombre":"PEPE EL PIYO Sanchez Pedroza",
#             "telefono":"449 405 26 64",
#             "correo":"maracas@gmail.com",
#             "parentesco":"padre",
#             "activo":true
#         }
#     ],
#     "historial_estados":[
#         {
#             "estado":"Activo",
#             "fecha":"2026-01-11T07:45:04.620118Z",
#             "justificacion":"Inscripción inicial"
#         }
#     ],
#     "evaluaciones_historico":[
#         {
#             "fecha":"2026-01-11T08:59:30.985196Z",
#             "estrato_resultante":"A",
#             "ingreso_mensual":40000.0,
#             "aprobado":null
#         },
#         {
#             "fecha":"2026-01-11T07:45:04.629659Z",
#             "estrato_resultante":"B",
#             "ingreso_mensual":15000.0,
#             "aprobado":true
#         }
#     ],
#     "metadata":{
#         "usuario_id":1,
#         "role":"Estudiante",
#         "activo_sistema":true
#     }
# }


#############################################################
#####3############# NUEVOS ENDPOINTS #########################
#############################################################

# 1. ESTUDIANTES - CREAR
curl -s -X POST http://127.0.0.1:8000/api/admin/students/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
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

# 2. ESTUDIANTES - BAJA (Calcula adeudos)
curl -s -X POST http://127.0.0.1:8000/api/admin/students/1001/baja/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "justificacion": "Falta de pago",
         "es_temporal": false,
         "fecha_baja": "2026-01-20"
     }'


# 3. TUTORES - CREAR Y VINCULAR
curl -s -X POST http://127.0.0.1:8000/api/admin/students/tutores/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "nombre": "Don Ramón",
         "apellido_paterno": "Valdés",
         "apellido_materno": "Castillo",
         "telefono": "555-888-999",
         "correo": "rondamon@vecindad.com",
         "estudiantes_ids": [1001, 1002],
         "parentesco": "Padre"
     }'


# 4. ESTRATOS - CREAR
curl -s -X POST http://127.0.0.1:8000/api/admin/estratos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "nombre": "F",
         "descripcion": "Beca Total",
         "porcentaje_descuento": 100.00,
         "color": "#888888",
         "ingreso_minimo": 0,
         "ingreso_maximo": 1000
     }'


# 5. EVALUACIONES - APROBAR
curl -s -X PUT http://127.0.0.1:8000/api/admin/evaluaciones/1/aprobar/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "aprobado": true,
         "comentarios_comision": "Aprobado",
         "estrato_id": 2
     }'


# 6. FINANZAS - GENERAR ADEUDOS MENSUALES
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/generar-mensual/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "mes": "2026-03"
     }'

# 7. FINANZAS - APLICAR RECARGOS
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/aplicar-recargos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{}'

# 8. FINANZAS - EXENTAR RECARGO
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/5/exentar/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "justificacion": "Error bancario"
     }'

# 9. FINANZAS - REGISTRAR PAGO MANUAL
curl -s -X POST http://127.0.0.1:8000/api/admin/pagos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "adeudo": 10,
         "monto": 2500.00,
         "metodo_pago": "Efectivo",
         "referencia": "Recibo 555",
         "recibido_por": "Caja 1"
     }'

# 10. CONFIGURACION - ACTUALIZAR
curl -s -X PUT http://127.0.0.1:8000/api/admin/configuracion-pago/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
         "dia_fin_ordinario": 15,
         "porcentaje_recargo": 12.50
     }'


# 11. COMEDOR - SUBIR MENU PDF
curl -s -X POST http://127.0.0.1:8000/api/admin/comedor/menus/ \
     -H "Authorization: Bearer <TOKEN>" \
     -F "semana_inicio=2026-02-01" \
     -F "semana_fin=2026-02-05" \
     -F "descripcion=Menu Feb 1" \
     -F "archivo_pdf=@/path/to/menu.pdf"

# 12. REPORTES
curl -s -X GET http://127.0.0.1:8000/api/admin/reportes/ingresos-estrato/ -H "Authorization: Bearer <TOKEN>"
curl -s -X GET http://127.0.0.1:8000/api/admin/reportes/recaudacion/ -H "Authorization: Bearer <TOKEN>"
curl -s -X GET http://127.0.0.1:8000/api/admin/comedor/alergias/ -H "Authorization: Bearer <TOKEN>"
