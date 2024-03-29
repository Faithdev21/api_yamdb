import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'reviews.apps.ReviewsConfig',
    'django_filters',
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

ROOT_URLCONF: str = 'api_yamdb.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
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

WSGI_APPLICATION: str = 'api_yamdb.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation

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

LANGUAGE_CODE: str = 'en-us'

TIME_ZONE: str = 'UTC'

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

# Static files (CSS, JavaScript, Images)

STATIC_URL: str = '/static/'

STATICFILES_DIRS = ((BASE_DIR / 'static/'),)

CSV_FILES_DIR = os.path.join(BASE_DIR, 'static/data')

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'
AUTH_USER_MODEL: str = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

PATH_CSV_FILES = {
    'category': str(BASE_DIR.joinpath('static/data/category.csv')),
    'genre': str(BASE_DIR.joinpath('static/data/genre.csv')),
    'title': str(BASE_DIR.joinpath('static/data/titles.csv')),
    'genretitle': str(BASE_DIR.joinpath('static/data/genre_title.csv')),
    'user': str(BASE_DIR.joinpath('static/data/users.csv')),
    'review': str(BASE_DIR.joinpath('static/data/review.csv')),
    'comment': str(BASE_DIR.joinpath('static/data/comments.csv')),
}
