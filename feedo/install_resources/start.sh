#!/bin/bash

cd /opt/app/

echo ">>> Collecting static"
python manage.py collectstatic --no-input

echo ">>> Applying migrations"
python manage.py migrate --no-input

echo ">>> Applying migrations"
python manage.py migrate --no-input

echo ">>> Starting uWSGI"

uwsgi \
    --ini /install_resources/uwsgi.ini \
    --wsgi-file /opt/app/wsgi.py

child=$!
wait "$child"
