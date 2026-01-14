#!/bin/bash
# Script para probar el endpoint de login con curl
## Por el momento no esta habilitado el JWT, pero esto sirve para probar que los endponts pueden
# recibir y repsonder correctamente.


## Retornará 200 OK -> pagina del index (login)
curl -X GET http://127.0.0.1:8000/ \
     -H "Content-Type: application/json"

# curl -X POST http://127.0.0.1:8000/api/token/ \
#      -H "Content-Type: application/json" \
#      -d '{"username": "adan", "password": "testpass123"}'


curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "adancpphack@gmail.com", "password": "testpass123"}'


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