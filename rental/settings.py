import mongoengine
from pymongo.mongo_client import MongoClient
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# La carpeta donde Django guardará los archivos subidos (media)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = 'django-insecure-34ue7ruie6lmq^j)@vpo15o)lhk23awwubco)d#e&r1nzx=tnn'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
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

ROOT_URLCONF = 'rental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', 'login'],
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

WSGI_APPLICATION = 'rental.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_DATABASE', 'postgres1_g650'),
        'USER': os.getenv('PG_USER', 'postgres1'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'L0a5bHI6mumDNrkzsIYIUBsglTamxYdn'),
        'HOST': os.getenv('PG_HOST', 'dpg-cspbbl3tq21c739qsa6g-a.virginia-postgres.render.com'),
        'PORT': os.getenv('PG_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',  # Requiere SSL
        },
    }
}

# Configuración para MongoDB usando mongoengine
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://SID2-USER:SID2-USER@project-sid2.ae5am.mongodb.net/Proyecto_SID2?retryWrites=true&w=majority')
mongoengine.connect(db='Proyecto_SID2', host=MONGO_URI)

# Configuración para verificar conexión con MongoDB
client = MongoClient(MONGO_URI)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
