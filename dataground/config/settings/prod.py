from .base import *
import secure_settings
import pymysql

pymysql.install_as_MySQLdb()
DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = []

DATABASES = secure_settings.DATABASES

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dataground',
#         'USER' : 'root',
#         'PASSWORD' : 'password',
#         'HOST' : '127.0.0.1',
#         'PORT' : '3306'
#     }
# }

API_KEY = secure_settings.API_KEY