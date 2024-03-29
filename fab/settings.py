import os
from decouple import config
import cloudinary
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%=r3#altd4m)_%_y7)y$xu+1bb&7ms!kd2h@vb-j*6jw38kkx6'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# cloudinary.config(cloud_name=config('cloud_name'),
#                   api_key=config('api_key'),
#                   api_secret=config('api_secret'))


ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": "AIzaSyDJ2EjngU1l9fOd0wPZpytw_1aC8_KRNnM"
}

# Application definition

INSTALLED_APPS = [
    'rest_framework.authtoken',
    # 'django.contrib.admin',
    'material.admin',
    'material.admin.default',
    'django.contrib.auth',
    'django_apscheduler',
    'rest_framework',
    'cloudinary',
    'fabapp.apps.FabappConfig',
    'exbrapp.apps.ExbrappConfig',
    'fabrapp.apps.FabrappConfig',
    'review.apps.ReviewConfig',
    'corsheaders',
    'fcm_django',
    'phonenumber_field',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework.authentication.BasicAuthentication',
     'rest_framework.authentication.SessionAuthentication',
     'rest_framework.authentication.TokenAuthentication')
}
AUTH_USER_MODEL = 'fabapp.User'

SCHEDULER_CONFIG = {
    "apscheduler.jobstores.default": {
        "class": "django_apscheduler.jobstores:DjangoJobStore"
    },
    'apscheduler.executors.processpool': {
        "type": "threadpool"
    },
}
SCHEDULER_AUTOSTART = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'fab.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fab',
        'USER': 'dbuser',
        'PASSWORD': 'Dbuser@1',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
# 'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'mf_dev_testing',
#         'USER': 'root',
#         'PASSWORD': 'java@123',
#         'HOST':'176.9.137.77',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
