from flightapi.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = "iloveicecream"

## Database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travisdb',
        'USER': 'postgres',
        'HOST': '127.0.0.1'
    }
}
