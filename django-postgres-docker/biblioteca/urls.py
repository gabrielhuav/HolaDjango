from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL pattern
    path('alumnos/registrar/', views.registrar_alumno, name='registrar_alumno'),
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    # Agregar las URLs para préstamos
    path('prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('prestamos/solicitar/', views.solicitar_prestamo, name='solicitar_prestamo'),
]