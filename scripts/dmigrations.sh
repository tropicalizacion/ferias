#!/bin/bash

docker-compose run --rm web python3 manage.py migrate
docker exec ferias_django_app python manage.py migrate
docker exec ferias_django_app python manage.py makemigrations marketplaces
docker exec ferias_django_app python manage.py makemigrations products
docker exec ferias_django_app python manage.py makemigrations crowdsourcing
docker exec ferias_django_app python manage.py makemigrations website
docker exec ferias_django_app python manage.py makemigrations users
docker exec ferias_django_app python manage.py makemigrations feed
docker exec ferias_django_app python manage.py makemigrations blog
# docker exec ferias_django_app python manage.py makemigrations content
docker exec ferias_django_app python manage.py makemigrations recipes
docker exec ferias_django_app python manage.py migrate

docker exec ferias_django_app python manage.py loaddata marketplaces
docker exec ferias_django_app python manage.py loaddata products
docker exec ferias_django_app python manage.py loaddata website
# docker exec ferias_django_app python manage.py loaddata crowdsourcing
# docker exec ferias_django_app python manage.py loaddata users
# docker exec ferias_django_app python manage.py loaddata feed
# docker exec ferias_django_app python manage.py loaddata content
docker-compose run --rm web python3 manage.py setup_wagtail_site
docker-compose run --rm web python3 manage.py makemigrations cms
