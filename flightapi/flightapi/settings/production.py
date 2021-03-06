from flightapi.settings.base import *
from dj_database_url import config, parse
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.getenv('SECRET_KEY')


DATABASES = {}
DATABASES['default'] = config(
    default=os.getenv('DATABASE_URL'), conn_max_age=600, ssl_require=True
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')