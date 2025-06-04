# gestion_piezas/forms.py
from django import forms
from .models import Pieza, Motor, Operario

class PiezaForm(forms.ModelForm):
    class Meta:
        model = Pieza
        fields = [
            'id_pieza',
            'codigo_pieza',
            'codigo_fabricante',
            'descripcion',
            'programa_cad',
            'material',
        ]
        labels = {
            'id_pieza': 'ID de Pieza (e.g., PZ000001)',
            'codigo_pieza': 'Código de Pieza',
            'codigo_fabricante': 'Código de Fabricante',
            'descripcion': 'Descripción',
            'programa_cad': 'Ruta Programa CAD (opcional)',
            'material': 'Material',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class MotorForm(forms.ModelForm):
    class Meta:
        model = Motor
        fields = [
            'id_motor',
            'descripcion',
            'num_piezas',
            'programa_cad',
            'tipo',
            'caballos_fuerza',
            'tipo_refrigeracion',
            'potencia_fiscal',
            'tipo_anclaje',
        ]
        labels = {
            'id_motor': 'ID de Motor (e.g., MT000001)',
            'descripcion': 'Descripción del Motor',
            'num_piezas': 'Número de Piezas',
            'programa_cad': 'Ruta Programa CAD (opcional)',
            'tipo': 'Tipo de Motor',
            'caballos_fuerza': 'Caballos de Fuerza (solo para motocicleta)',
            'tipo_refrigeracion': 'Tipo de Refrigeración (solo para motocicleta)',
            'potencia_fiscal': 'Potencia Fiscal (solo para automóvil)',
            'tipo_anclaje': 'Tipo de Anclaje (solo para automóvil)',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'num_piezas': forms.NumberInput(attrs={'min': 1}),
            'caballos_fuerza': forms.NumberInput(attrs={'min': 1}),
            'potencia_fiscal': forms.NumberInput(attrs={'min': 1}),
        }

class OperarioForm(forms.ModelForm):
    class Meta:
        model = Operario
        fields = ['id_operario', 'nombre', 'sueldo']
        widgets = {
            'id_operario': forms.TextInput(attrs={'placeholder': 'Ej: OP000001'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo del operario'}),
            'sueldo': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Ej: 18000.50'}),
        }
        labels = {
            'id_operario': 'ID del Operario',
            'nombre': 'Nombre Completo',
            'sueldo': 'Sueldo (MXN)',
        }