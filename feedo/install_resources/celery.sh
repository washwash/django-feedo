#!/bin/bash

cd /opt/app/

echo ">>> Starting Celery"
celery -A applications.async_update worker -l info &

echo ">>> Starting Celery Beat"
celery beat -A applications.async_update -l info &

child=$!
wait "$child"