"""
Django settings for taxi project.

Generated by 'django-admin startproject' using Django 2.0.3.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
with open('secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
]

INSTALLED_APPS = [
    "django.contrib.admindocs",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_SSL_REDIRECT = False

X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = "taxi.urls"

TEMPLATES = []

WSGI_APPLICATION = 'taxi.wsgi.application'

DATABASES = {}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True