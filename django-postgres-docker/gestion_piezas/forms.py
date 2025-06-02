# gestion_piezas/forms.py
from django import forms
from .models import Pieza

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