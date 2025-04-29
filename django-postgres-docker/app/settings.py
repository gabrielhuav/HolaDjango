import os # Necesitas importar os para acceder a las variables de entorno
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent # Asumiendo que settings.py está en un subdirectorio 'app'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Deberías generar una clave secreta real y preferiblemente leerla desde una variable de entorno
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-fallback-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
# Lee DEBUG desde una variable de entorno, por defecto True para desarrollo
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# 👇 AÑADE ESTA LÍNEA: Define los hosts permitidos
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# Si DEBUG es False, esta lista DEBE contener los hosts/dominios correctos.
# Puedes leerla desde una variable de entorno también:
# ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1').split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'biblioteca', 
    # 👇 Asegúrate de que 'app' es el nombre correcto de tu app Django
    # Si tu app está en otro directorio, ajústalo (ej. 'mi_app.apps.MiAppConfig')
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 👇 Asegúrate de que 'app.urls' sea el nombre correcto de tu archivo urls principal
ROOT_URLCONF = 'app.urls' # O el nombre de tu proyecto si settings.py está dentro de él

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Si tienes un directorio de plantillas global, añádelo aquí:
        # 'DIRS': [BASE_DIR / 'templates'],
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 👇 Asegúrate de que 'app.wsgi.application' sea correcto
WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

# 👇 ACTUALIZA ESTO para usar variables de entorno
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca_cendi',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# Django 4.0 cambió el nombre de USE_L10N a USE_FORMAT_SETTING
# Comenta/descomenta según tu versión de Django
# USE_L10N = True
USE_FORMAT_SETTING = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = '/static/'
# Opcional: Define dónde recogerá collectstatic los archivos estáticos
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'