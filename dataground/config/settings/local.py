from .base import * 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataground',
        'USER' : 'encore',
        'PASSWORD' : 'encore!@#',
        'HOST' : '127.0.0.1',
        'PORT' : '3306'
    }
}
INSTALLED_APPS.append("django_extensions")
