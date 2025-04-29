from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/registrar/', views.registrar_alumno, name='registrar_alumno'),
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
]