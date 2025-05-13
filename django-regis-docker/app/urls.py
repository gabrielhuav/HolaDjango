from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('set', views.set_value, name='set_value'),
    path('get', views.get_value, name='get_value'),
    path('get-all', views.get_all_keys, name='get_all_keys'),
    path('delete', views.delete_value, name='delete_value'),
    path('load-products', views.load_products, name='load_products'),
    path('load-all-products', views.load_all_products, name='load_all_products'),
]