from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
]