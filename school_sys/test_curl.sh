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


# ADMIN ESTRATOS -> CREAR
# Crea un nuevo nivel socioeconomico
curl -s -X POST http://127.0.0.1:8000/api/admin/estratos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "nombre": "A+",
         "descripcion": "Nivel Alto Plus",
         "porcentaje_descuento": 0,
         "color": "#000000",
         "ingreso_minimo": 100000,
         "ingreso_maximo": 999999
     }'

# Aprobar desde el admin e
# Aprueba o rechaza una evaluacion socioeconomica
curl -s -X PUT http://127.0.0.1:8000/api/admin/evaluaciones/1/aprobar/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "aprobado": true,
         "comentarios_comision": "Aprobado por unanimidad",
         "estrato_id": 2
     }'

# ADMIN BAJA ESTUDIANTE
# Procesa la baja (temporal/definitiva), calcula adeudos y "desactiva" usuario
curl -s -X POST http://127.0.0.1:8000/api/admin/students/220548/baja/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "justificacion": "Cambio de residencia",
         "es_temporal": false,
         "fecha_baja": "2026-01-20"
     }'


# Genera los adeudos de colegiatura para el mes especificado para todos los alumnos activos
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/generar-mensual/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "mes": "2026-02"
     }'

# 5. ADMIN APLICAR RECARGOS
# Aplica recargos (10% + $125) a todos los adeudos vencidos que no tengan recargo aun
curl -s -X POST http://127.0.0.1:8000/api/admin/adeudos/aplicar-recargos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{}'

# 6. ADMIN CONFIGURACION PAGO
# Actualiza las reglas globales de cobranza
# JSON Body: dia_inicio_ordinario, dia_fin_ordinario, porcentaje_recargo, monto_fijo_recargo
curl -s -X PUT http://127.0.0.1:8000/api/admin/configuracion-pago/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{
         "dia_inicio_ordinario": 1,
         "dia_fin_ordinario": 10,
         "porcentaje_recargo": 15.00,
         "monto_fijo_recargo": 150.00
     }'

# 7. ADMIN REPORTE INGRESOS POR ESTRATO
# Retorna el total recaudado agrupado por estrato socioeconomico
curl -s -X GET http://127.0.0.1:8000/api/admin/reportes/ingresos-estrato/ \
     -H "Authorization: Bearer <access_token>"

# 8. ADMIN ALUMNOS CON ALERGIAS
# Lista alumnos que tienen registradas alergias alimentarias (para comedor)
curl -s -X GET http://127.0.0.1:8000/api/admin/comedor/alergias/ \
     -H "Authorization: Bearer <access_token>"
