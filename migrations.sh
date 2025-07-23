#!/bin/bash
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
