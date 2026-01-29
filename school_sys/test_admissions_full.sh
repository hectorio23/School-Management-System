#!/bin/bash

# Configuración base
BASE_URL="http://127.0.0.1:8000/api/admission"
RAND_ID=$(( ( RANDOM % 10000 ) + 1000 ))
EMAIL="test_${RAND_ID}@example.com"
PASSWORD="SecurePassword123!"

# Generador de CURP válido (Aprox)
CURP="TEST$((RANDOM%90+10))0101HDFRRN01"
TUTOR1_CURP="TUTR$((RANDOM%90+10))0101MDFRRN01"
TUTOR2_CURP="TUTR$((RANDOM%90+10))0101HDFRRN02"

echo ">>> [STEP 1] REGISTRATION INITIATE"
RES_INIT=$(curl -s -X POST "$BASE_URL/register/initiate/" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

CODE=$(echo $RES_INIT | jq -r '.code_debug')
echo "Verification Code: $CODE"

if [ "$CODE" == "null" ]; then
    echo "Error initiating registration: $RES_INIT"
    exit 1
fi

echo ">>> [STEP 2] REGISTRATION CONFIRM"
RES_CONFIRM=$(curl -s -X POST "$BASE_URL/register/confirm/" \
    -H "Content-Type: application/json" \
    -d "{
        \"email\": \"$EMAIL\",
        \"code\": \"$CODE\",
        \"nombre\": \"AspiranteTest\",
        \"apellido_paterno\": \"Apellido\",
        \"apellido_materno\": \"Materno\",
        \"curp\": \"$CURP\"
    }")

FOLIO=$(echo $RES_CONFIRM | jq -r '.folio')
echo "Registered Folio: $FOLIO"

if [ "$FOLIO" == "null" ]; then
    echo "Error confirming registration: $RES_CONFIRM"
    exit 1
fi

echo ">>> [STEP 3] LOGIN"
RES_LOGIN=$(curl -s -X POST "$BASE_URL/login/" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

ACCESS_TOKEN=$(echo $RES_LOGIN | jq -r '.tokens.access')
echo "Access Token: ${ACCESS_TOKEN:0:20}..."

if [ "$ACCESS_TOKEN" == "null" ]; then
    echo "Error logging in: $RES_LOGIN"
    exit 1
fi

AUTH_HEADER="Authorization: Bearer $ACCESS_TOKEN"

echo ">>> [STEP 4] PHASE 1: Personal Data & Tutors"
# Note: In serializers.py, Phase 1 now advancing to Phase 2 automatically
RES_PHASE1=$(curl -s -X PUT "$BASE_URL/aspirante/$FOLIO/phase1/" \
    -H "$AUTH_HEADER" \
    -H "Content-Type: application/json" \
    -d "{
        \"curp\": \"$CURP\",
        \"fecha_nacimiento\": \"2015-05-20\",
        \"sexo\": \"M\",
        \"direccion\": \"Av. Tecnológico 123\",
        \"telefono\": \"4491234567\",
        \"escuela_procedencia\": \"Primaria Central\",
        \"promedio_anterior\": 9.5,
        \"nivel_ingreso\": \"PRIMARIA\",
        \"tutores\": [
            {
                \"nombre\": \"Tutor Uno\",
                \"apellido_paterno\": \"Paterno\",
                \"apellido_materno\": \"Materno\",
                \"email\": \"tutor1_${RAND_ID}@test.com\",
                \"numero_telefono\": \"4497654321\",
                \"curp\": \"$TUTOR1_CURP\",
                \"parentesco\": \"Padre\"
            },
            {
                \"nombre\": \"Tutor Dos\",
                \"apellido_paterno\": \"Paterno2\",
                \"apellido_materno\": \"Materno2\",
                \"email\": \"tutor2_${RAND_ID}@test.com\",
                \"numero_telefono\": \"4490000000\",
                \"curp\": \"$TUTOR2_CURP\",
                \"parentesco\": \"Madre\"
            }
        ]
    }")
echo $RES_PHASE1 | jq .

# Obtenemos los IDs de los tutores para la fase 3 si es necesario
# Pero la vista actual soporta subida por tutor.id
echo ">>> [FINAL CHECK] Applicant Status"
curl -s -H "$AUTH_HEADER" "$BASE_URL/dashboard/$FOLIO/" | jq .

echo ">>> [STEP 5] PHASE 2: Socioeconomic"
curl -s -X PUT "$BASE_URL/aspirante/$FOLIO/phase2/" \
    -H "$AUTH_HEADER" \
    -H "Content-Type: application/json" \
    -d "{
        \"ingreso_mensual_familiar\": 25000.00,
        \"ocupacion_padre\": \"Ingeniero\",
        \"ocupacion_madre\": \"Doctora\",
        \"tipo_vivienda\": \"Propia\",
        \"miembros_hogar\": 4,
        \"vehiculos\": 2,
        \"internet_encasa\": true
    }" | jq .

echo ">>> [STEP 6] PHASE 3: Documentation Upload (REAL FILES)"
# Para subir archivos reales usamos -F (multipart/form-data)
# Nota: La vista espera 'curp_pdf', 'acta_nacimiento', etc. del alumno
# Y para los tutores 'tutor_<id>_<field>' o genéricos si es uno solo.

# Obtenemos los IDs de los tutores de la respuesta de la Fase 1
TUTOR_IDS=$(echo $RES_PHASE1 | jq -r '.data.tutores[].id')
TUTOR_ID_1=$(echo $TUTOR_IDS | awk '{print $1}')
TUTOR_ID_2=$(echo $TUTOR_IDS | awk '{print $2}')

echo "Uploading files for Tutor 1 (ID: $TUTOR_ID_1) and Tutor 2 (ID: $TUTOR_ID_2)..."

curl -s -X PUT "$BASE_URL/aspirante/$FOLIO/phase3/" \
    -H "$AUTH_HEADER" \
    -F "aceptacion_reglamento=true" \
    -F "autorizacion_imagen=true" \
    -F "curp_pdf=@test_doc.pdf" \
    -F "acta_nacimiento=@test_doc.pdf" \
    -F "foto_credencial=@test_img.jpg" \
    -F "boleta_ciclo_anterior=@test_doc.pdf" \
    -F "boleta_ciclo_actual=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_acta_nacimiento_tutor=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_comprobante_domicilio_tutor=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_foto_fachada_domicilio=@test_img.jpg" \
    -F "tutor_${TUTOR_ID_1}_comprobante_ingresos=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_carta_ingresos=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_ine_tutor=@test_img.jpg" \
    -F "tutor_${TUTOR_ID_1}_contrato_arrendamiento_predial=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_carta_bajo_protesta=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_1}_curp_pdf_tutor=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_acta_nacimiento_tutor=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_comprobante_domicilio_tutor=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_foto_fachada_domicilio=@test_img.jpg" \
    -F "tutor_${TUTOR_ID_2}_comprobante_ingresos=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_carta_ingresos=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_ine_tutor=@test_img.jpg" \
    -F "tutor_${TUTOR_ID_2}_contrato_arrendamiento_predial=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_carta_bajo_protesta=@test_doc.pdf" \
    -F "tutor_${TUTOR_ID_2}_curp_pdf_tutor=@test_doc.pdf" | jq .

echo ">>> [FINAL VERIFICATION] Final Status in Panel"
curl -s -H "$AUTH_HEADER" "$BASE_URL/dashboard/$FOLIO/" | jq .

echo ">>> [STEP 7] DASHBOARD TEST"
curl -s -H "$AUTH_HEADER" "$BASE_URL/dashboard/$FOLIO/" | jq .
