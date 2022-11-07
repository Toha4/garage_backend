import os
from datetime import timedelta
from pathlib import Path

import environ
import ldap
from django_auth_ldap.config import ActiveDirectoryGroupType
from django_auth_ldap.config import LDAPSearch

# Set environment
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=str, default="localhost, 127.0.0.1").split(", ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "authentication",
    "core",
    "orders",
    "warehouse",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


CORS_ORIGIN_ALLOW_ALL = env("CORS_ORIGIN_ALLOW_ALL", cast=bool, default=False)
CORS_ALLOW_CREDENTIALS = env("CORS_ALLOW_CREDENTIALS", cast=bool, default=True)
CORS_ORIGIN_WHITELIST = env("CORS_ORIGIN_WHITELIST", cast=str, default="http://localhost:3000").split(", ")


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": env.db(),
    "mssql_sync": {
        "NAME": "putewka",
        "ENGINE": "sql_server.pyodbc",
        "HOST": env("DATABASE_MSSQL_HOST", cast=str),
        "USER": env("DATABASE_MSSQL_USER", cast=str),
        "PASSWORD": env("DATABASE_MSSQL_PASSWORD", cast=str),
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            "unicode_results": True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Asia/Vladivostok"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = " ".join((DATE_FORMAT, TIME_FORMAT))

SERIALIZER_DATE_PARAMS = dict(format="%d.%m.%Y", input_formats=["%d.%m.%Y", "iso-8601"])
SERIALIZER_DATETIME_PARAMS = dict(format="%d.%m.%Y %H:%M", input_formats=["%d.%m.%Y %H:%M", "iso-8601"])


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", cast=str, default=os.path.join(BASE_DIR, "static"))

# Media files

MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT", cast=str, default=os.path.join(BASE_DIR, "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "app.pagination.BasePagination",
    "PAGE_SIZE": 50,
    "DATE_FORMAT:": DATE_FORMAT,
    "DATE_INPUT_FORMATS": [DATE_FORMAT, "iso-8601"],
    "TIME_FORMAT": TIME_FORMAT,
    "DATETIME_FORMAT": DATETIME_FORMAT,
}


# Set authentication
AUTHENTICATION_BACKENDS = [
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Set LDAP

AUTH_LDAP_SERVER_URI = env("AUTH_LDAP_SERVER_URI", cast=str, default="")
AUTH_LDAP_BIND_DN = env("AUTH_LDAP_BIND_DN", cast=str, default="")
AUTH_LDAP_BIND_PASSWORD = env("AUTH_LDAP_BIND_PASSWORD", cast=str, default="")
AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=mupts,dc=office", ldap.SCOPE_SUBTREE, "sAMAccountName=%(user)s")

AUTH_LDAP_TIMEOUT = env("AUTH_LDAP_TIMEOUT", cast=float, default=10.0)
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_NETWORK_TIMEOUT: AUTH_LDAP_TIMEOUT,
    ldap.OPT_TIMEOUT: AUTH_LDAP_TIMEOUT,
}

AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "initials": "initials",
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("dc=mupts,dc=office", ldap.SCOPE_SUBTREE, "(objectCategory=Group)")
AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")

# Active Directory groups for mirror import in the django

AUTH_LDAP_MIRROR_GROUPS = [
    "СМиТ",
]

# JWT
AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("SIMPLE_JWT_SIGNING_KEY", cast=str, default=SECRET_KEY),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": AUTH_HEADER_NAME,
    "USER_ID_FIELD": "pk",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "REFRESH_COOKIE_NAME": "refresh_garage",
}

# Custom user model
AUTH_USER_MODEL = "authentication.CustomUser"
