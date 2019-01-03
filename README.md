# Flight Booking API
[![Build Status](https://travis-ci.org/imisi-akande/flight_booking_api.svg?branch=develop)](https://travis-ci.org/imisi-akande/flight_booking_api)
[![Coverage Status](https://coveralls.io/repos/github/imisi-akande/flight_booking_api/badge.svg)](https://coveralls.io/github/imisi-akande/flight_booking_api)

## Description
This repository will contain the API endpoints and models for the Fastpace Flight booking that enables users to book, purchase, and reserve tickets for a flight. The system was built using the Django rest framework. Other technologies
used are Celery and Redis to anchor concurrent tasks.


### Getting Started

- Clone the repository:
> $ git clone https://github.com/imisi-akande/flight_booking_api

- Open the project directory:
> $ cd flight_booking_api/flightapi

### Set up environment variables
- To set up environment variables, define the following in a `.env` file:

- DB_NAME - The name of your database
-  DB_PORT - The port connection of your database
-  DB_USER - Name of the database user with privileges
-  HOST - Name of the local host
-  SECRET_KEY - Parameter used for encryption and decryption
-  JWT_SECRET_KEY - Parameters to authenticate server APi
-  SENDGRID_USERNAME -  Your Email delivery service username
- SENDGRID_PASSWORD - Your Email delivery service password
- SENDGRID_API_KEY - Your API key on the service settings

### Set up Database
- Create a database:
> $ createdb db_name
- Run migrations
> $ python manage.py migrate

### Running the app locally
- To run tests:
> $ python manage.py test
- Run the app:
> $ python manage.py runserver

### Create a Superuser account
- To create a super user account for accessing the admin dashboard, run the following command:
> python manage.py createsuperuser
- Enter your email
- You can log into the admin dashboard using those credentials on `http://127.0.0.1:8000/admin/`

## Application Setup
- Install `PostgreSQL` and `Redis`
- Run `redis-server` to start the redis server.
- Run `chmod +x ./setup.sh` on a separate terminal to execute the bash scripts.
- Run `source setup.sh` to setup your development environment.
- Run `pip install -r requirements.txt` to install all dependencies
- Run python manage.py runserver to start the server
- Run `celery -A config worker -l info` on a separate terminal to start the celery server
- Run `celery -A config beat` to start celery beat

## Deployment
[FastPace Heroku link](https://fastpaceflight.herokuapp.com/api/v1/)
