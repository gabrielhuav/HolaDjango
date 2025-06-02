# gestion_piezas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('insertar/', views.insertar_pieza, name='insertar_pieza'),
    path('insertada_ok/', views.pieza_insertada_ok, name='pieza_insertada_ok'),
]