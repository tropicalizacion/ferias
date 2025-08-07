#!/bin/bash
# This script runs migrations and loads initial data into the Django application
# Only needed if not using Docker
python manage.py migrate
python manage.py makemigrations marketplaces
python manage.py makemigrations products
python manage.py makemigrations crowdsourcing
python manage.py makemigrations website
python manage.py makemigrations users
python manage.py makemigrations feed
python manage.py makemigrations blog
python manage.py makemigrations content
python manage.py makemigrations recipes
python manage.py migrate

python manage.py loaddata marketplaces
python manage.py loaddata products
python manage.py loaddata website
python manage.py loaddata crowdsourcing
python manage.py loaddata users
python manage.py loaddata feed
python manage.py loaddata content
