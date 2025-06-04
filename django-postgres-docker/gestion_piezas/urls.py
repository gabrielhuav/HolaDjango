from django.urls import path
from . import views

urlpatterns = [
    path('insertar-pieza/', views.insertar_pieza, name='insertar_pieza'),
    path('pieza-insertada/', views.pieza_insertada_ok, name='pieza_insertada_ok'),
    path('insertar-motor/', views.insertar_motor, name='insertar_motor'),
    path('motor-insertado/', views.motor_insertado_ok, name='motor_insertado_ok'),
    path('insertar-operario/', views.insertar_operario, name='insertar_operario'),
    path('operario-insertado/', views.operario_insertado_ok, name='operario_insertado_ok'),
]