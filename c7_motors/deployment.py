import os 
from .settings import *
from .settings import BASE_DIR 
import stripe 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s!vl(b5$%6q#izpl_oq!y!14gony(_s*o&&13@$=q+7=^)v4)n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#The trusted urls and domains from which requests can come into our applictation 
ALLOWED_HOSTS = ['.railway.app']


DEBUG = False


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))#MS ADDED
Temp_Path = os.path.realpath('.')# MS ADDED
index_path =  os.path.join(os.path.dirname(os.path.dirname(__file__)),'templates')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH ,'templates')],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#STATIC_ROOT = os.path.join(BASE_DIR , 'staticfiles')

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR , 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  


MEDIA_URL='/media/'
MEDIA_ROOT= os.path.join(BASE_DIR , 'media')  


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
    }
}


#Payment By STRIPE
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY =os.environ.get('STRIPE_SECRET_KEY')