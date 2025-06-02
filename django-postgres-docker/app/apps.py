# app/apps.py
from django.apps import AppConfig

class AppNameConfig(AppConfig): # Or whatever you named your class, e.g., AppConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    # verbose_name = "My Application" # Example of other configs