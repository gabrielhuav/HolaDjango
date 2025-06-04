# gestion_piezas/models.py
from django.db import models

class Pieza(models.Model):
    MATERIAL_CHOICES = [
        ('AL', 'Aluminio'), # From SQL: ENUM('AL', 'AC', 'PL')
        ('AC', 'Acero'),   # From SQL: ENUM('AL', 'AC', 'PL')
        ('PL', 'Plástico'), # From SQL: ENUM('AL', 'AC', 'PL')
    ]

    id_pieza = models.CharField(max_length=8, primary_key=True) # From SQL: id_pieza CHAR(8) PRIMARY KEY
    codigo_pieza = models.CharField(max_length=8) # From SQL: codigo_pieza VARCHAR(8) NOT NULL
    codigo_fabricante = models.CharField(max_length=3) # From SQL: codigo_fabricante CHAR(3) NOT NULL
    descripcion = models.TextField() # From SQL: descripcion TEXT NOT NULL
    programa_cad = models.CharField(max_length=150, blank=True, null=True) # From SQL: programa_cad VARCHAR(150)
    material = models.CharField(max_length=2, choices=MATERIAL_CHOICES) # From SQL: material ENUM('AL', 'AC', 'PL') NOT NULL

    def __str__(self):
        return f"{self.id_pieza} - {self.descripcion}"

class Motor(models.Model):
    TIPO_CHOICES = [
        ('Motocicleta', 'Motocicleta'),
        ('Automóvil', 'Automóvil'),
    ]
    
    id_motor = models.CharField(max_length=8, primary_key=True)
    descripcion = models.TextField()
    num_piezas = models.IntegerField()
    programa_cad = models.CharField(max_length=150, blank=True, null=True)
    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)
    caballos_fuerza = models.IntegerField(blank=True, null=True)
    tipo_refrigeracion = models.CharField(max_length=50, blank=True, null=True)
    potencia_fiscal = models.IntegerField(blank=True, null=True)
    tipo_anclaje = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.id_motor} - {self.descripcion}"
    
class Operario(models.Model):
    id_operario = models.CharField(max_length=8, primary_key=True)
    nombre = models.CharField(max_length=100)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.id_operario} - {self.nombre}"