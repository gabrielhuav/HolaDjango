from django import forms
from .models import Alumno, CicloEscolar

class AlumnoForm(forms.ModelForm):
    """
    Formulario para registrar y editar alumnos.
    """
    class Meta:
        model = Alumno
        fields = ['codigo_alumno', 'nombre', 'apellido_paterno', 'apellido_materno', 'escuela', 'ciclo']
        widgets = {
            'codigo_alumno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ALU2025001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del alumno'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno'}),
            'escuela': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. CENDI IPN'}),
            'ciclo': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(AlumnoForm, self).__init__(*args, **kwargs)
        # Establecer valores iniciales o por defecto
        if not self.initial.get('escuela'):
            self.initial['escuela'] = 'CENDI IPN'