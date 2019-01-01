web: gunicorn flightapi.wsgi --log-file -
worker: celery -A flightapi worker --beat --loglevel=info 