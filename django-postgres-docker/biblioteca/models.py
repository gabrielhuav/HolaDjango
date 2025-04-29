from django.db import models

class CicloEscolar(models.Model):
    nombre_ciclo = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __str__(self):
        return self.nombre_ciclo
    
    class Meta:
        verbose_name_plural = "Ciclos Escolares"

class Alumno(models.Model):
    codigo_alumno = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    escuela = models.CharField(max_length=100, default='CENDI IPN')
    ciclo = models.ForeignKey(CicloEscolar, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    class Meta:
        verbose_name_plural = "Alumnos"

class Editorial(models.Model):
    codigo_editorial = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Editoriales"

class Autor(models.Model):
    codigo_autor = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50, blank=True, null=True)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno or ''} {self.apellido_materno or ''}"
    
    class Meta:
        verbose_name_plural = "Autores"

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Especialidades"

class Libro(models.Model):
    codigo_libro = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=200)
    numero_paginas = models.PositiveIntegerField()
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    autores = models.ManyToManyField(Autor, related_name='libros')
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Libros"

class Prestamo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    devuelto = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.alumno.nombre}"
    
    class Meta:
        verbose_name_plural = "Préstamos"
        unique_together = ('alumno', 'libro', 'fecha_prestamo')
        
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.fecha_devolucion and self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError('La fecha de devolución debe ser posterior a la fecha de préstamo.')