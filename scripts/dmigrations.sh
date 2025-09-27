#!/bin/bash

docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py migrate
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations marketplaces
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations products
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations crowdsourcing
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations website
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations cms_pages
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations users
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations feed
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations blog
# docker exec -e -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations content
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py makemigrations recipes
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py migrate

# Initialize Wagtail default pages (home/blog) after migrating
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py init_wagtail
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata marketplaces
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata products
docker exec -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata website
# docker exec -e -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata crowdsourcing
# docker exec -e -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata users
# docker exec -e -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata feed
# docker exec -e -e PYTHONWARNINGS=ignore ferias_django_app python manage.py loaddata content