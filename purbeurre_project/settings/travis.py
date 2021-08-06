from . import *

SECRET_KEY = "travis_secret_key"
# print(BASE_DIR)
BASE_DIR = "/home/travis/build/tsering10/P10_deployment/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}