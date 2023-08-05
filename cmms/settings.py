"""
Django settings for cmms project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from os import getenv
from pathlib import Path

import dj_database_url

from cmms.enums import UserType
from cmms.menu import Item


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(getenv("DJANGO_DEBUG", "true"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY", "django-insecure-3a+f4k+o0s5gxi*j1v@%rhd@p#v3os!e%*skb#g0slq605bl07" if DEBUG else ""
)
if not SECRET_KEY and not DEBUG:
    raise RuntimeError("You must set DJANGO_SECRET_KEY in production mode!")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"] + getenv("DJANGO_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "tailwind",
    "cmms",
    "django_browser_reload",
    "phonenumber_field",
    "widget_tweaks",
    "graphene_django",
    "django_htmx",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_AGE = 60 * 60 * 24  # 1 day in seconds
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = "cmms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

TEMPLATE_LOADERS = ('django.template.loaders.app_directories.load_template_source',)

WSGI_APPLICATION = "cmms.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR.parent / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    ),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = getenv("DJANGO_STATIC", None)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1",
]

TAILWIND_APP_NAME = "cmms"

AUTH_USER_MODEL = "cmms.User"

AUTHENTICATION_BACKENDS = ["cmms.auth.CMMSBackend"]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

APPEND_SLASH = False

MENU_ITEMS = [
    Item("Dashboard", "/dashboard/home", "home"),
    Item("Employees", "/dashboard/users", "person", roles=[UserType.ADMIN]),
    Item("Spareparts", "/dashboard/spareparts", "settings", roles=[UserType.ADMIN]),
    Item("Agent / Supplier", "/dashboard/agent", "folder_supervised", roles=[UserType.ADMIN]),
    Item("Work Order", "/dashboard/workorder", "assignment"),
    Item("Work Center", "/dashboard/workplace", "group", roles=[UserType.ADMIN]),
    Item("Equipment", "/dashboard/equipment", "home_repair_service"),
    Item("Maintenance", "/dashboard/maintenance", "build"),
    Item("Report", "/dashboard/report", "summarize"),
    Item("Asset Report", "/dashboard/report", "speed"),
]

GRAPHENE = {"SCHEMA": "cmms.schema.schema"}
