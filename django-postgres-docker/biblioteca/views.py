from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import Alumno, CicloEscolar, Libro, Prestamo
from .forms import AlumnoForm

def index(request):
    """Vista de página inicial"""
    total_alumnos = Alumno.objects.count()
    total_libros = Libro.objects.count() if hasattr(Libro.objects, 'count') else 0
    total_prestamos = Prestamo.objects.count() if hasattr(Prestamo.objects, 'count') else 0
    prestamos_activos = Prestamo.objects.filter(devuelto=False).count() if hasattr(Prestamo.objects, 'filter') else 0
    
    context = {
        'total_alumnos': total_alumnos,
        'total_libros': total_libros,
        'total_prestamos': total_prestamos,
        'prestamos_activos': prestamos_activos,
    }
    
    return render(request, 'biblioteca/index.html', context)

def registrar_alumno(request):
    """Vista para registrar un nuevo alumno"""
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save()
            messages.success(request, f'¡Alumno {alumno.nombre} registrado correctamente!')
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()
    
    return render(request, 'biblioteca/registrar_alumno.html', {
        'form': form,
    })

def lista_alumnos(request):
    """Vista para listar todos los alumnos"""
    alumnos = Alumno.objects.all().order_by('apellido_paterno')
    return render(request, 'biblioteca/listar_alumnos.html', {
        'alumnos': alumnos
    })

def lista_prestamos(request):
    """Vista provisional para listar préstamos"""
    # Vista sencilla para evitar el error NoReverseMatch
    prestamos = []
    if hasattr(Prestamo.objects, 'all'):
        prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    
    return render(request, 'biblioteca/listar_prestamos.html', {
        'prestamos': prestamos
    })

def solicitar_prestamo(request):
    """Vista provisional para solicitar préstamos"""
    # Vista sencilla para evitar el error NoReverseMatch
    return render(request, 'biblioteca/solicitar_prestamo.html', {
        'form': None
    })