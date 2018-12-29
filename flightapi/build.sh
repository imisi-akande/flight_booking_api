# stops execution if there is an error
set -e
python manage.py makemigrations
python manage.py migrate
coverage manage.py test