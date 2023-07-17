from .base import *
import secure_settings
import pymysql

pymysql.install_as_MySQLdb()
DEBUG = True

ALLOWED_HOSTS = ['*']

# DATABASES = secure_settings.DATABASES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataground',
        'USER' : 'root',
        'PASSWORD' : 'password',
        'HOST' : '127.0.0.1',
        'PORT' : '3306'
    }
}

KEY = secure_settings.KEYS