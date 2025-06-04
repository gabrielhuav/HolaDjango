# gestion_piezas/views.py
from django.shortcuts import render, redirect
from .forms import PiezaForm, MotorForm, OperarioForm
from .models import Pieza, Motor, Operario # Ensure Pieza is imported if you add a success message listing pieces

def insertar_pieza(request):
    if request.method == 'POST':
        form = PiezaForm(request.POST)
        if form.is_valid():
            form.save()
            # You can redirect to a success page or the same page with a success message
            # For now, let's redirect to a simple success indication (or list view if you create one)
            return redirect('pieza_insertada_ok') # We'll define this URL name later
    else:
        form = PiezaForm()
    return render(request, 'gestion_piezas/insertar_pieza.html', {'form': form})

def pieza_insertada_ok(request):
    # A simple view to confirm insertion
    # Optionally, you could list all Piezas here
    # piezas = Pieza.objects.all()
    # return render(request, 'gestion_piezas/pieza_insertada_ok.html', {'piezas': piezas})
    return render(request, 'gestion_piezas/pieza_insertada_ok.html')

def insertar_motor(request):
    if request.method == 'POST':
        form = MotorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('motor_insertado_ok')
    else:
        form = MotorForm()
    return render(request, 'gestion_piezas/insertar_motor.html', {'form': form})

def motor_insertado_ok(request):
    return render(request, 'gestion_piezas/motor_insertado_ok.html')

def insertar_operario(request):
    if request.method == 'POST':
        form = OperarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('operario_insertado_ok')
    else:
        form = OperarioForm()
    return render(request, 'gestion_piezas/insertar_operario.html', {'form': form})

def operario_insertado_ok(request):
    return render(request, 'gestion_piezas/operario_insertado_ok.html')