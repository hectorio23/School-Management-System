from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

AUTH_USER_MODEL = "users.User"
SECRET_KEY = os.getenv('KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

# For JWT Tokens settings 
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('ACCESS_TOKEN_LIFETIME'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('REFRESH_TOKEN_LIFETIME'))),
    'ALGORITHM': os.getenv('ALGORITHM'),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


# Application definition
INSTALLED_APPS = [
    'users',
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'estudiantes',
    'rest_framework',
    'comedor',
    'pagos',
    'admissions',
]

JAZZMIN_SETTINGS = {
    "site_title": "Admin TI",
    "site_header": "Panel TI",
    "site_brand": "Plataforma Interna",
    "welcome_sign": "Administración del sistema",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
    },
    "theme": "cyborg",  # darkly, flatly, lumen, cyborg, etc
}

JAZZMIN_SETTINGS["hide_apps"] = []
JAZZMIN_SETTINGS["hide_models"] = []
JAZZMIN_SETTINGS["show_ui_builder"] = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



################### EMAIL ###################

# EMAIL_HOST = "<server_smtp>"          
# EMAIL_PORT = 587 # TLS
# EMAIL_HOST_USER = "<user_mail>"
# EMAIL_HOST_PASSWORD = "<password_>"
# EMAIL_USE_TLS = True  
# # EMAIL_USE_SSL = True  

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = 'school_sys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'school_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

## To execute the project, you need to install the following dependencies:
# sudo pacman -S python-mysqlclient python-mysql-connector (Arch Linux)

# pip install mysqlclient
# or 
# pip install pymysql (you will need to add to your __init__.py:
# - CREATE DATABASE school_sys CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'), 
        'PASSWORD': os.getenv('DB_PASSWORD'), 
        'HOST': os.getenv('DB_HOST'),
        'PORT': int(os.getenv('DB_PORT')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
