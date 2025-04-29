#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# Importar los modelos necesarios
from biblioteca.models import CicloEscolar, Alumno, Editorial, Autor, Especialidad, Libro, Prestamo

def insertar_prestamo_gabriel():
    """Registra a Gabriel como alumno, crea el libro 'Risitos de Oro' y registra un préstamo."""
    
    # Fecha actual proporcionada
    fecha_actual = datetime.strptime("2025-04-28 22:10:55", "%Y-%m-%d %H:%M:%S").date()
    fecha_devolucion = fecha_actual + timedelta(days=14)  # 2 semanas para devolución
    
    try:
        print("Iniciando proceso de registro de préstamo...")
        
        # 1. Crear o recuperar ciclo escolar
        ciclo, creado = CicloEscolar.objects.get_or_create(
            nombre_ciclo="2025-2026",
            defaults={
                'fecha_inicio': datetime(2025, 8, 15).date(),
                'fecha_fin': datetime(2026, 7, 31).date()
            }
        )
        print(f"✓ Ciclo escolar {'creado' if creado else 'recuperado'}: {ciclo.nombre_ciclo}")
        
        # 2. Crear o recuperar alumno Gabriel
        alumno, creado = Alumno.objects.get_or_create(
            nombre="Gabriel",
            defaults={
                'codigo_alumno': "GABR2025",
                'apellido_paterno': "Huerta",
                'apellido_materno': "Alvarez",
                'escuela': "CENDI IPN",
                'ciclo': ciclo
            }
        )
        print(f"✓ Alumno {'creado' if creado else 'recuperado'}: {alumno.nombre} {alumno.apellido_paterno}")
        
        # 3. Crear o recuperar editorial
        editorial, creado = Editorial.objects.get_or_create(
            nombre="Cuentos Infantiles",
            defaults={
                'codigo_editorial': "CI2025",
                'direccion': "Ciudad de México",
                'telefono': "555-123-4567"
            }
        )
        print(f"✓ Editorial {'creada' if creado else 'recuperada'}: {editorial.nombre}")
        
        # 4. Crear o recuperar autor
        autor, creado = Autor.objects.get_or_create(
            nombre="Anónimo",
            defaults={
                'codigo_autor': "AN001",
                'apellido_paterno': "",
                'apellido_materno': "",
                'email': "cuentos.anonimos@literatura.org"
            }
        )
        print(f"✓ Autor {'creado' if creado else 'recuperado'}: {autor.nombre}")
        
        # 5. Crear o recuperar especialidad
        especialidad, creado = Especialidad.objects.get_or_create(
            nombre="Cuentos Clásicos",
            defaults={
                'descripcion': "Cuentos tradicionales y fábulas para niños"
            }
        )
        print(f"✓ Especialidad {'creada' if creado else 'recuperada'}: {especialidad.nombre}")
        
        # 6. Crear o recuperar libro Risitos de Oro
        libro, creado = Libro.objects.get_or_create(
            titulo="Risitos de Oro",
            defaults={
                'codigo_libro': "RO2025",
                'numero_paginas': 32,
                'especialidad': especialidad,
                'editorial': editorial
            }
        )
        if creado:
            libro.autores.add(autor)
        print(f"✓ Libro {'creado' if creado else 'recuperado'}: {libro.titulo}")
        
        # 7. Crear préstamo
        prestamo, creado = Prestamo.objects.get_or_create(
            alumno=alumno,
            libro=libro,
            fecha_prestamo=fecha_actual,
            defaults={
                'fecha_devolucion': fecha_devolucion,
                'devuelto': False
            }
        )
        
        # 8. Mostrar información del préstamo
        print("\n✅ PRÉSTAMO REGISTRADO EXITOSAMENTE:")
        print(f"   Usuario: gabrielhuav")
        print(f"   Fecha y hora: {fecha_actual} 22:10:55")
        print(f"   Alumno: {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
        print(f"   Código alumno: {alumno.codigo_alumno}")
        print(f"   Libro: {libro.titulo}")
        print(f"   Código libro: {libro.codigo_libro}")
        print(f"   Fecha de préstamo: {prestamo.fecha_prestamo}")
        print(f"   Fecha de devolución: {prestamo.fecha_devolucion}")
        print(f"   Estado: {'Prestado' if not prestamo.devuelto else 'Devuelto'}")
        
    except Exception as e:
        print(f"❌ Error durante el proceso: {str(e)}")

if __name__ == "__main__":
    insertar_prestamo_gabriel()