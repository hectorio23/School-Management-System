#!/bin/bash
# Script para probar el endpoint de login con curl
## Por el momento no esta habilitado el JWT, pero esto sirve para probar que los endponts pueden
# recibir y repsonder correctamente.

BASE_URL="http://127.0.0.1:8000"

echo "=== Test 1: Login exitoso (jerry2201) ==="
curl -X POST "${BASE_URL}/students/login/" \
  -H "Content-Type: application/json" \
  -d '{"hash": "c66b7c9f9b90e7f70a8f4e2017a4f4a90a1a9dac21204015f2805ca4f37e5915"}' \
  -w "\n\nStatus: %{http_code}\n"

echo -e "\n=== Test 2: Login con hash inválido ==="
curl -X POST "${BASE_URL}/students/login/" \
  -H "Content-Type: application/json" \
  -d '{"hash": "hash_invalido"}' \
  -w "\n\nStatus: %{http_code}\n"

echo -e "\n=== Test 3: Login sin hash ==="
curl -X POST "${BASE_URL}/students/login/" \
  -H "Content-Type: application/json" \
  -d '{}' \
  -w "\n\nStatus: %{http_code}\n"
