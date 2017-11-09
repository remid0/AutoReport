#!/bin/bash
sudo apt update
sudo apt-get install redis
pip install -r requirements.tkt
python manage.py migrate
redis-server &
celery -A server worker -l info &
python manage.py runserver 0.0.0.0:8000