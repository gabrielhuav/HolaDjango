from django.db import models

class CicloEscolar(models.Model):
    id_ciclo = models.BigAutoField(primary_key=True) # Explicitly define the PK matching the DB column name
    nombre_ciclo = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __str__(self):
        return self.nombre_ciclo
    
    class Meta:
        verbose_name_plural = "Ciclos Escolares"
        db_table = 'ciclos_escolares'
        managed = False

class Alumno(models.Model):
    id_alumno = models.BigAutoField(primary_key=True) # Explicitly define the PK
    codigo_alumno = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    escuela = models.CharField(max_length=100, default='CENDI IPN')
    ciclo = models.ForeignKey(CicloEscolar, on_delete=models.CASCADE, db_column='id_ciclo')
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    class Meta:
        verbose_name_plural = "Alumnos"
        db_table = 'alumnos'
        managed = False

class Editorial(models.Model):
    id_editorial = models.BigAutoField(primary_key=True) # Explicitly define the PK
    codigo_editorial = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Editoriales"
        db_table = 'editoriales'
        managed = False

class Autor(models.Model):
    id_autor = models.BigAutoField(primary_key=True) # Explicitly define the PK
    codigo_autor = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50, blank=True, null=True)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno or ''} {self.apellido_materno or ''}"
    
    class Meta:
        verbose_name_plural = "Autores"
        db_table = 'autores'
        managed = False

class Especialidad(models.Model):
    id_especialidad = models.BigAutoField(primary_key=True) # Explicitly define the PK
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Especialidades"
        db_table = 'especialidades'
        managed = False

class Libro(models.Model):
    id_libro = models.BigAutoField(primary_key=True) # Explicitly define the PK
    codigo_libro = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=200)
    numero_paginas = models.PositiveIntegerField()
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, db_column='id_especialidad')
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, db_column='id_editorial')
    autores = models.ManyToManyField(Autor, through='LibroAutor', related_name='libros')
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Libros"
        db_table = 'libros'
        managed = False

class LibroAutor(models.Model):
    # This model uses a composite primary key defined in Meta, so no single PK field is needed here.
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, db_column='id_libro')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, db_column='id_autor')
    
    class Meta:
        db_table = 'libros_autores'
        unique_together = ('libro', 'autor') # Defines the composite primary key
        managed = False

class Prestamo(models.Model):
    id_prestamo = models.BigAutoField(primary_key=True) # Explicitly define the PK
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, db_column='id_libro')
    fecha_prestamo = models.DateField(auto_now_add=True) # Note: DB default is CURRENT_DATE, Django default is auto_now_add
    fecha_devolucion = models.DateField(blank=True, null=True)
    devuelto = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.alumno.nombre}"
    
    class Meta:
        verbose_name_plural = "Préstamos"
        db_table = 'prestamos'
        unique_together = ('alumno', 'libro', 'fecha_prestamo')
        managed = False