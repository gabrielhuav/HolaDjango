#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, date

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# Importar los modelos necesarios
from biblioteca.models import CicloEscolar

def crear_ciclo_escolar():
    """Crea un ciclo escolar para pruebas si no existe ninguno."""
    
    # Verificar si ya existen ciclos escolares
    ciclos_count = CicloEscolar.objects.count()
    
    if ciclos_count == 0:
        print("No hay ciclos escolares registrados. Creando uno nuevo...")
        
        # Crear ciclo escolar para el periodo actual
        ciclo = CicloEscolar.objects.create(
            nombre_ciclo="2025-2026",
            fecha_inicio=date(2025, 8, 1),
            fecha_fin=date(2026, 7, 31)
        )
        
        print(f"✅ Ciclo escolar creado: {ciclo.nombre_ciclo}")
    else:
        print(f"Ya existen {ciclos_count} ciclos escolares en la base de datos.")
        for ciclo in CicloEscolar.objects.all():
            print(f"- {ciclo.nombre_ciclo}: {ciclo.fecha_inicio} al {ciclo.fecha_fin}")

if __name__ == "__main__":
    crear_ciclo_escolar()