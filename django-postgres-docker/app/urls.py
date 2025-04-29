from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('biblioteca/', include('biblioteca.urls')),
    path('', include('biblioteca.urls')),  # Para que funcione desde la raíz
]