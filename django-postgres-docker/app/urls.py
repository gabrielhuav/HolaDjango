# app/urls.py (your project's main urls.py)
from django.contrib import admin
from django.urls import path, include # Make sure include is imported
from . import views # Assuming views.py is in the same 'app' directory for the root path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), # Your existing root path
    path('piezas/', include('gestion_piezas.urls')), # For the 'gestion_piezas' app
]