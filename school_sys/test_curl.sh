#!/bin/bash
# Script para probar el endpoint de login con curl
## Por el momento no esta habilitado el JWT, pero esto sirve para probar que los endponts pueden
# recibir y repsonder correctamente.


## Retornará 200 OK -> pagina del index (login)
curl -X GET http://127.0.0.1:8000/ \
     -H "Content-Type: application/json"

curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "adan", "password": "testpass123"}'


curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "adancpphack@gmail.com", "password": "testpass123"}'


curl -X GET http://127.0.0.1:8000/students/info/ \
     -H "Authorization: Bearer <ACCESS_TOKEN>"