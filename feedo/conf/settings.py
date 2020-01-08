from pathlib import Path

import os
from configurations import Configuration


class BaseConfiguration(Configuration):
    BASE_DIR = Path(__file__).parents[1]

    SECRET_KEY = '5pn$@5g11$*6a3k(ys0ytr=c+&b!(!u-f+y#5ph2c)xz$ko7&b'
    DEBUG = True

    ALLOWED_HOSTS = []
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'applications.index',
        'applications.authentication',
        'applications.feed',
        'applications.subscription',
        'applications.async_update',
        'applications.base',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'applications.authentication.middlewares.LoginRequiredMiddleware'
    ]

    STATIC_URL = '/static/'
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'environment': 'feedo.conf.jinja2.environment',
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]
            }
        },
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

    WSGI_APPLICATION = 'wsgi.application'

    # postgres =  # create user feedo with password '1234';
    # CREATE
    # ROLE
    # postgres =  # create database feedo;
    # CREATE
    # DATABASE
    # postgres =  # GRANT ALL PRIVILEGES ON DATABASE "feedo" to feedo
    DATABASES = {
        'default': {
            'NAME': os.getenv('FEEDO_DATABASE_NAME'),
            'ENGINE': 'django.db.backends.postgresql',
            'USER': os.getenv('FEEDO_DATABASE_USER'),
            'PASSWORD': os.getenv('FEEDO_DATABASE_PASSWORD')
        },
    }
    TIME_ZONE = os.getenv('FEEDO_TIME_ZONE', 'UTC')
    USE_TZ = True
    ROOT_URLCONF = 'conf.urls'

    AUTH_USER_MODEL = 'auth.User'
    LOGIN_URL = 'index:index'
    LOGIN_REDIRECT_URL = 'index:index'
    LOGOUT_REDIRECT_URL = 'index:index'
    IGNORE_AUTHENTICATION_REQUIRED_VIEWS = (
        'authentication:sign_in',
        'authentication:sign_up',
        'index:index',
    )


class Dev(BaseConfiguration):
    DEBUG = True


class Test(BaseConfiguration):
    pass
