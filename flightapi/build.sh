# stops execution if there is an error
set -e
python manage.py makemigrations
python manage.py migrate
coverage run --source='.' manage.py test