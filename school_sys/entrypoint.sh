#!/bin/bash
set -e

echo "=== Iniciando SMS Backend ==="

# 1. Esperar a que la base de datos (MariaDB) esté disponible
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-3306}"

echo "[+] Esperando conexión a la base de datos en ${DB_HOST}:${DB_PORT}..."
python << 'EOF'
import os
import sys
import time
import socket

host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', 3306))
start_time = time.time()
timeout = 60

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"[+] Conexión exitosa con MariaDB en {host}:{port}")
            sys.exit(0)
    except OSError:
        if time.time() - start_time > timeout:
            print(f"[!] Tiempo de espera agotado conectando a {host}:{port}", file=sys.stderr)
            sys.exit(1)
        print(f"[-] Esperando a MariaDB ({host}:{port})...")
        time.sleep(2)
EOF

# 2. Aplicar migraciones de Django
echo "[+] Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

# 3. Recopilar archivos estáticos para Nginx
echo "[+] Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# 4. Iniciar Gunicorn
echo "[+] Iniciando servidor Gunicorn en el puerto 8000..."
exec gunicorn school_sys.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
