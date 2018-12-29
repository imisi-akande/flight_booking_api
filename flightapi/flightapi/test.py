from flightapi.test import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = ')uya@is*$8!1luag=_v1jnog0yo)7*&c%$sn_x3qn#ysg6uzt6'
## Database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travisdb',
        'USER': 'AkandeImisioluwa',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}
