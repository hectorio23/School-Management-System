#!/bin/bash
set -e

#################################################################33
############################### NOTA @###########################
#################################################################33

## USUARIO DE PRUEBA: Estudiante
# - host: http://127.0.0.1:8000 < en producción será el puerto 443 (HTTPS) >
# - email: adancpphack@gmail.com
# - password: testpass123 

# Una vez que el servicio mariadb esta ejecutandose en segundo plano, lo primero es inizializarlo
#  y crear el usuario correspondiente y la ruta de trabajo
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing MariaDB..."
    mariadb-install-db --user=mysql --datadir=/var/lib/mysql
    chown -R mysql:mysql /var/lib/mysql
fi

# ejecutando servicio
echo "[+] - Starting MariaDB..."
mysqld_safe --datadir=/var/lib/mysql &
mariadb_pid=$!

echo "[-] - Waiting for MariaDB to be ready..."
until mysqladmin ping --silent; do
    echo "Waiting for localhost..."
    sleep 2
done

# creando el usuaio con sus credenciales y asignandole la base de datos
echo "[+] - Configuring Database..."
mysql -u root -e "CREATE DATABASE IF NOT EXISTS school_sys CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -e "CREATE USER IF NOT EXISTS 'adan'@'localhost' IDENTIFIED BY 'kernelripper';"
mysql -u root -e "GRANT ALL PRIVILEGES ON school_sys.* TO 'adan'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"



# importando TODAS las tablas del dump <docs/school_sys.sql>
echo "[+] - Importing SQL dump..."
mysql -u root school_sys < docs/school_sys.sql

echo "[+] - Database READY to use."

# RADYYyy..
echo "[+] - Starting Django Server..."
exec python school_sys/manage.py runserver 0.0.0.0:8000


