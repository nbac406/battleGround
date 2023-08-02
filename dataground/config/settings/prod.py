from .base import *
import secure_settings
import pymysql
import os

pymysql.install_as_MySQLdb()
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = secure_settings.DATABASES

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.environ['DB_NAME'],
#         'USER' : os.environ['DB_USER'],
#         'PASSWORD' : os.environ['DB_PASSWORD'],
#         'HOST' : os.environ['DB_HOST'],
#         'PORT' : os.environ['DB_PORT']
#     }
# }


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'dataground',
#        'USER' : 'root',
#        'PASSWORD' : 'password',
#        'HOST' : '127.0.0.1',
#        'PORT' : '3306',
#    }
#}

## 실험용
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'test2',
#         'USER' : 'root',
#         'PASSWORD' : '1234',
#         'HOST' : '127.0.0.1',
#         'PORT' : '4000',
#     }
# }

KEY = secure_settings.KEYS