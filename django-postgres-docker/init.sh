#!/bin/bash
set -e

# Esperar a que PostgreSQL esté listo
echo "Esperando a que PostgreSQL esté listo..."
while ! pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

# Ejecutar comandos de Django
echo "Ejecutando migraciones de Django..."
python manage.py makemigrations
python manage.py migrate

echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000