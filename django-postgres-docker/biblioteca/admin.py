from django.contrib import admin
from .models import CicloEscolar, Alumno, Editorial, Autor, Especialidad, Libro, Prestamo

@admin.register(CicloEscolar)
class CicloEscolarAdmin(admin.ModelAdmin):
    list_display = ('nombre_ciclo', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre_ciclo',)

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('codigo_alumno', 'nombre', 'apellido_paterno', 'apellido_materno', 'escuela', 'ciclo')
    search_fields = ('codigo_alumno', 'nombre', 'apellido_paterno', 'apellido_materno')
    list_filter = ('escuela', 'ciclo')

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ('codigo_editorial', 'nombre', 'telefono')
    search_fields = ('codigo_editorial', 'nombre')

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('codigo_autor', 'nombre', 'apellido_paterno', 'apellido_materno', 'email')
    search_fields = ('codigo_autor', 'nombre', 'apellido_paterno', 'apellido_materno', 'email')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('codigo_libro', 'titulo', 'numero_paginas', 'especialidad', 'editorial')
    search_fields = ('codigo_libro', 'titulo')
    list_filter = ('especialidad', 'editorial')
    filter_horizontal = ('autores',)

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'devuelto')
    search_fields = ('alumno__nombre', 'libro__titulo')
    list_filter = ('devuelto', 'fecha_prestamo', 'fecha_devolucion')