from flightapi.test import *

DEBUG = True

ALLOWED_HOSTS = ['*']

## Database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travisdb',
        'USER': 'postgres',
        'HOST': '127.0.0.1'
    }
}
