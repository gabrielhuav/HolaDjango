#!/usr/bin/env python
import os
import sys
import django
import time

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# Importar los modelos necesarios
from biblioteca.models import Alumno, CicloEscolar
from django.db import connection

def verificar_tablas():
    """Verificar la estructura de las tablas y los datos en la base de datos."""
    
    # 1. Imprimir información de los modelos
    print("\n=== INFORMACIÓN DE MODELOS DJANGO ===")
    print(f"Modelo Alumno:")
    print(f"  - Tabla real: {Alumno._meta.db_table}")
    print(f"  - Campos:")
    for field in Alumno._meta.fields:
        print(f"    - {field.name}: {field.get_internal_type()}")
    
    print(f"\nModelo CicloEscolar:")
    print(f"  - Tabla real: {CicloEscolar._meta.db_table}")
    print(f"  - Campos:")
    for field in CicloEscolar._meta.fields:
        print(f"    - {field.name}: {field.get_internal_type()}")
    
    # 2. Listar todas las tablas en la base de datos
    print("\n=== TABLAS EN LA BASE DE DATOS ===")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tablas = cursor.fetchall()
        for tabla in tablas:
            print(f"  - {tabla[0]}")
    
    # 3. Verificar datos en modelos Django
    print("\n=== DATOS EN MODELOS DJANGO ===")
    alumnos_django = Alumno.objects.all()
    print(f"Alumnos en Django: {alumnos_django.count()}")
    for alumno in alumnos_django:
        print(f"  - ID: {alumno.id}, Código: {alumno.codigo_alumno}, Nombre: {alumno.nombre} {alumno.apellido_paterno}")
    
    ciclos_django = CicloEscolar.objects.all()
    print(f"\nCiclos escolares en Django: {ciclos_django.count()}")
    for ciclo in ciclos_django:
        print(f"  - ID: {ciclo.id}, Nombre: {ciclo.nombre_ciclo}, Periodo: {ciclo.fecha_inicio} a {ciclo.fecha_fin}")
    
    # 4. Verificar datos directamente en la base de datos
    print("\n=== DATOS DIRECTOS EN BASE DE DATOS ===")
    
    with connection.cursor() as cursor:
        # Verificar tabla biblioteca_alumno
        print("Tabla biblioteca_alumno:")
        try:
            cursor.execute("SELECT COUNT(*) FROM biblioteca_alumno;")
            count = cursor.fetchone()[0]
            print(f"  - Total registros: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, codigo_alumno, nombre, apellido_paterno FROM biblioteca_alumno LIMIT 5;")
                for row in cursor.fetchall():
                    print(f"  - ID: {row[0]}, Código: {row[1]}, Nombre: {row[2]} {row[3]}")
        except Exception as e:
            print(f"  - Error: {str(e)}")
        
        # Verificar tabla alumnos (del SQL original)
        print("\nTabla alumnos:")
        try:
            cursor.execute("SELECT COUNT(*) FROM alumnos;")
            count = cursor.fetchone()[0]
            print(f"  - Total registros: {count}")
            
            if count > 0:
                cursor.execute("SELECT id_alumno, codigo_alumno, nombre, apellido_paterno FROM alumnos LIMIT 5;")
                for row in cursor.fetchall():
                    print(f"  - ID: {row[0]}, Código: {row[1]}, Nombre: {row[2]} {row[3]}")
        except Exception as e:
            print(f"  - Error: {str(e)}")
    
    # 5. Sugerir solución
    print("\n=== DIAGNÓSTICO ===")
    print("Si estás viendo datos en los modelos Django pero no en la tabla SQL 'alumnos',")
    print("hay una discrepancia entre el nombre de la tabla que Django está usando y el nombre esperado.")
    print("Para solucionar esto, debes actualizar el modelo Alumno en Django para que use la tabla 'alumnos'")
    print("o modificar las migraciones para crear la estructura correcta de tablas.")

if __name__ == "__main__":
    print("Verificando tablas y datos en la base de datos...")
    verificar_tablas()
