#!/bin/bash

BASE_URL="http://127.0.0.1:8000/api/admission"
RAND_ID=$(( ( RANDOM % 10000 ) + 1000 ))
EMAIL="full_test_${RAND_ID}@example.com"
PASSWORD="SecurePassword123!"

echo ">>> [STEP 0] AUTH FLOW"
RES=$(curl -s -X POST "$BASE_URL/auth/send-code/" -H "Content-Type: application/json" -d "{\"email\": \"$EMAIL\"}")
CODE=$(echo $RES | jq -r '.code_debug')
curl -s -X POST "$BASE_URL/auth/verify-code/" -H "Content-Type: application/json" -d "{\"email\": \"$EMAIL\", \"code\": \"$CODE\"}" > /dev/null

echo ">>> [STEP 1] REGISTRATION"
RES_REG=$(curl -s -X POST "$BASE_URL/register/" -H "Content-Type: application/json" -d "{
    \"user_data\": {\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"},
    \"nombre\": \"AspiranteFull\",
    \"apellido_paterno\": \"Test\",
    \"apellido_materno\": \"Test\"
}")
FOLIO=$(echo $RES_REG | jq -r '.folio')
echo "Registered Folder: $FOLIO"

echo ">>> [STEP 2] PHASE 1: Personal Data & Tutors"
curl -s -X PUT "$BASE_URL/me/$FOLIO/phase1/" -H "Content-Type: application/json" -d "{
    \"curp\": \"CURP${RAND_ID}TEST\",
    \"fecha_nacimiento\": \"2015-01-01\",
    \"genero\": \"M\",
    \"direccion\": \"Calle Falsa 123\",
    \"tutores\": [
        {
            \"nombre\": \"Tutor1\",
            \"apellido_paterno\": \"Paterno\",
            \"numero_telefono\": \"1234567890\",
            \"email\": \"tutor${RAND_ID}@test.com\",
            \"parentesco\": \"Padre\"
        }
    ]
}" | jq .

echo ">>> [STEP 3] PHASE 2: Socioeconomic"
curl -s -X PUT "$BASE_URL/me/$FOLIO/phase2/" -H "Content-Type: application/json" -d "{
    \"ingreso_mensual_familiar\": 15000.50,
    \"tipo_vivienda\": \"Propia\",
    \"miembros_hogar\": 4,
    \"vehiculos\": 1,
    \"internet_encasa\": true
}" | jq .

echo ">>> [STEP 4] PHASE 3: Legal Checks & Docs"
# Test failure first (missing checks)
echo "Testing check validation (expected failure):"
curl -s -X PUT "$BASE_URL/me/$FOLIO/phase3/" -H "Content-Type: application/json" -d "{\"aceptacion_reglamento\": false}" | jq .

echo "Testing successful docs & checks:"
# Note: Since uploading files with curl is complex in one line, we test the logic and booleans.
# We skip the file binary for now but it's supported in the view.
curl -s -X PUT "$BASE_URL/me/$FOLIO/phase3/" -H "Content-Type: application/json" -d "{
    \"aceptacion_reglamento\": true,
    \"autorizacion_imagen\": true
}" | jq .

echo ">>> [STEP 5] PHASE 4: Admin Payment"
curl -s -X POST "$BASE_URL/admin/$FOLIO/mark-paid/" -H "Content-Type: application/json" -d "{
    \"admin_name\": \"Hector Admin\",
    \"metodo_pago\": \"Transferencia\"
}" | jq .

echo ">>> [FINAL CHECK] Current status"
curl -s "$BASE_URL/me/$FOLIO/" | jq .
