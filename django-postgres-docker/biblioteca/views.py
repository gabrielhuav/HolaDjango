from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Alumno, CicloEscolar
from .forms import AlumnoForm

def registrar_alumno(request):
    ciclos = CicloEscolar.objects.all()
    
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
        'ciclos': ciclos,
    })

def lista_alumnos(request):
    alumnos = Alumno.objects.all().order_by('apellido_paterno')
    return render(request, 'biblioteca/lista_alumnos.html', {
        'alumnos': alumnos
    })