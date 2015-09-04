"""
Django settings for dagger project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0^f3^b$$du=2u%1q7ybe2gvsx%@^7t+92s#q3smpm_f-y==^n#'

private_information = False
try:
    from dagger.private import DATABASE, SITE_NAME, SECRET_KEY, PRODUCTION
    private_information = True
except: pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if private_information:
    DEBUG = not PRODUCTION

ALLOWED_HOSTS = [ 'localhost' ]
if private_information:
    ALLOWED_HOSTS.append( SITE_NAME )

# Application definition
SITE_ID = 1
STATIC_ROOT = BASE_DIR + '/static'

CRISPY_TEMPLATE_PACK = 'bootstrap'

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'fluent_comments',
    'crispy_forms',
    'django_comments',
    'django.contrib.sites',
    'django_extensions',
    'account',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'knowledge',
    'handouts'
)

LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                },
            'simple': {
                'format': '%(levelname)s %(message)s'
                },
            },
        'handlers': {
            'null': {
                'level':'DEBUG',
                'class':'django.utils.log.NullHandler',
                },
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
                },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                }
            },
        'loggers': {
            'django': {
                'handlers':['null'],
                'propagate': True,
                'level':'INFO',
                },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
                },
            'cprepa.custom': {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
                }
            }
        }
COMMENTS_APP = 'fluent_comments'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
)

ROOT_URLCONF = 'dagger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR + '/dagger/templates/' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'pinax_theme_bootstrap.context_processors.theme',
                'account.context_processors.account',
            ],
        },
    },
]

WSGI_APPLICATION = 'dagger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}
if private_information:
    DATABASES['default'] = DATABASE

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
