"""
Django settings for application project.

Generated by "django-admin startproject" using Django 4.1.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from redislite import Redis
from pathlib import Path
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEYS")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = str(getenv("DEBUG")) == "True"

ALLOWED_HOSTS = ["*"]

# Application definition

GRAPPELLI_ADMIN_TITLE = "My admin"

AVATAR_GRAVATAR_DEFAULT = "monsterid"

from bleach.css_sanitizer import CSSSanitizer

ALLOWED_HTML_TAGS = {
    "p",
    "a",
    "img",
    "br",
    "em",
    "i",
    "b",
    "strong",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "blockquote",
    "u",
    "strike",
    "span",
    "sup",
    "hr",
    "div",
    "font",
}

ALLOWED_HTML_ATTRIBUTES = [
    "align",
    "class",
    "style",
    "color",
    "href",
    "target",
    "src",
]

CSS_SANITIZER = CSSSanitizer(
    allowed_css_properties=[
        "background-color",
        "color",
        "font-family",
        "font-size",
        "font-style",
        "height",
        "margin",
        "padding",
        "text-align",
        "vertical-align",
        "line-height",
        "width",
    ]
)

LOGIN_URL = "user:login"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

INSTALLED_APPS = [
    "widget_tweaks",
    "django_gravatar",
    "django_select2",
    "compressor",
    "captcha",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "users",
    "posts",
    # "notifications",
]

CAPTCHA_IMAGE_SIZE = (250,75)

CAPTCHA_LENGTH = 8

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)


SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": Redis(BASE_DIR / "cache.db"),
    }
}

ROOT_URLCONF = "application.urls"

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

WSGI_APPLICATION = "application.wsgi.application"

AUTH_USER_MODEL = "users.User"

GRAVATAR_DEFAULT_IMAGE = "retro"

GRAVATAR_DEFAULT_RATING = "g"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": getenv("DBASE_NAME"),
        "USER": getenv("DBASE_USERNAME"),
        "PASSWORD": getenv("DBASE_PASSWORD"),
        "HOST": getenv("DBASE_HOST"),
        "PORT": "3306",
    }
}


if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            "TEST": {
                "NAME": BASE_DIR / "testing.sqlite3",
            },
        },
    }
    INSTALLED_APPS += "debug_toolbar",
    MIDDLEWARE += "debug_toolbar.middleware.DebugToolbarMiddleware",


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = (BASE_DIR / "static",)

STATIC_ROOT = BASE_DIR / "staticfiles"

ITEM_PER_PAGE = 15

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = getenv("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = getenv("EMAIL_PASSWORD")
