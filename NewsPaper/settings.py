"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import _locale

# from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [

    'modeltranslation',  # обязательно впишите его перед админом

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    ### 'django.contrib.flatpages',
    ### 'news.templatetags',
    ### 'django_extensions',

    'django_filters',

    'sign',
    'protect',
    'django_apscheduler',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    'news.apps.NewsConfig',
    'rest_framework',
]

SITE_ID = 1

# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'

# если задача не выполняется за 25 секунд, то она автоматически снимается,
# можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # to activate lang localization
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware',

    'news.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,  # disabled to make pypugjs work
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_FRAMEWORK = {
   'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
   'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
   'PAGE_SIZE': 10,
   'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ]
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {'timeout': 5, },
        # 'TIME_ZONE': 'UTC',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # was 'none'
ACCOUNT_FORMS = {'signup': 'sign.forms.BasicSignupForm'}
# позволит избежать дополнительных действий и активирует аккаунт сразу,
# как только мы перейдем по ссылке
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# количество дней, в течение которых будет доступна ссылка на подтверждение регистрации
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

EMAIL_HOST = os.getenv('EMAIL_HOST')  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
# ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user,
# иными словами, это всё то что идёт до собаки
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # пароль от почты
EMAIL_SUBJECT_PREFIX = '[Django Tutorial] --> '
# Яндекс и Mail.Ru используют ssl, подробнее о том, что это, почитайте в дополнительных источниках,
# но включать его здесь обязательно
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

ADMINS = [
    ('romab-gm', os.getenv('ADMIN_1_EMAIL')),
    ('romab-ya', os.getenv('ADMIN_2_EMAIL')),
    # список всех админов в формате ('имя', 'их почта')
]
SERVER_EMAIL = DEFAULT_FROM_EMAIL

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

_locale._getdefaultlocale = (lambda *args: ['en_us', 'utf8'])

# LANGUAGE_CODE = 'en-us'

FILE_CHARSET = 'utf8'

TIME_ZONE = 'UTC'  # 'Europe/Moscow'

USE_I18N = True

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский'),
    # ('de', 'Deutsch'),
]
MODELTRANSLATION_LANGUAGES = ('en', 'ru')

USE_L10N = True

USE_TZ = True

USE_DEPRECATED_PYTZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

### from pypugjs.ext.django.compiler import enable_pug_translations
### enable_pug_translations()

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        # Указываем, куда будем сохранять кэшируемые файлы! Не забываем 
        # создать папку cache_files внутри папки с manage.py!
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

BLUE = "\033[34m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
PURPLE = "\033[35m"
ORIGIN_COLOR = "\033[0m"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 'simple': {
        #     'format': f'{ORIGIN_COLOR}%(asctime)s :{GREEN}: %(levelname)s :{ORIGIN_COLOR}: %(message)s'
        # },
        'verbose': {
            'format': f'{YELLOW}%(levelname)s {ORIGIN_COLOR} %(asctime)s :: \
                       %(pathname)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'error_format': {
            'format': f'{RED}%(levelname)s :{ORIGIN_COLOR}: %(asctime)s \
                       %(pathname)s %(module)s %(process)d %(thread)d %(message)s %(exc_info)s'
        },
        'info_format': {
            'format': f'{YELLOW}%(levelname)s :{ORIGIN_COLOR}: %(asctime)s %(module)s %(message)s'
        },
        'error_file_format': {
            'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s %(exc_info)s'
        },
        'security_format': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'mail_format': {
            'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },

    },
    'handlers': {
        # 'console': {
        #     'level': 'DEBUG',
        #     'filters': ['require_debug_true'],
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'simple'
        # },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_info': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'info_format',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'error_file_format',
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'security_format',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail_format',
        }
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console', 'console_warning', 'console_error', 'file_info'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        'django.request': {
            'handlers': ['mail_admins', 'file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['mail_admins', 'file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': ORIGIN_COLOR + '{asctime} -- ' + GREEN + '{levelname}'
#                       + ORIGIN_COLOR + ' -- {message}',
#             'style': '{',
#         },
#         'forinfo': {
#             'format': ORIGIN_COLOR + '{asctime} -- ' + BLUE + '{levelname}'
#                       + ORIGIN_COLOR + ' -- {module} : {message}',
#             'style': '{',
#         },
#         'forwarning': {
#             'format': ORIGIN_COLOR + '{asctime} -- ' + YELLOW + '{levelname}'
#                       + ORIGIN_COLOR + ' -- {pathname} : {message}',
#             'style': '{',
#         },
#         'forerror': {
#             'format': ORIGIN_COLOR + '{asctime} -- ' + PURPLE + '{levelname}'
#                       + ORIGIN_COLOR + ' -- {pathname} / {exc_info} :{message}',
#             'style': '{',
#         },
#         'security': {
#             'format': ORIGIN_COLOR + '{asctime} -- ' + RED + '{levelname}'
#                       + ORIGIN_COLOR + ' -- {module} : {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#
#     },
#     'handlers': {
#         'general': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filters': ['require_debug_false'],
#             'filename': 'general.log',
#             'formatter': 'standard'
#         },
#         'errors': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'error.log',
#             'formatter': 'forerror'
#         },
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter': 'forwarning',
#         },
#         'security': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'security.log',
#             'formatter': 'forwarning',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['errors', 'mail_admins', 'general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.server': {
#             'handlers': ['errors', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django.template': {
#             'handlers': ['errors'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django.db.backends': {
#             'handlers': ['errors'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django.security.*': {
#             'handlers': ['security'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
