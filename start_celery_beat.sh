#!/bin/bash

while true; do
    PG_STATUS=`PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -p 5432 -U $DATABASE_USER -w $DATABASE_PASSWORD -c '\l \q'  | grep postgres | wc -l`
    if ! [ "$PG_STATUS" -eq "0" ]; then
       break
    fi
    echo "Waiting Database Setup"
    sleep 10
done

PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -U $DATABASE_USER -W $DATABASE_PASSWORD -c "CREATE DATABASE ${DATABASE_NAME} OWNER ${DATABASE_USER}"


python3 manage.py makemigrations
python3 manage.py migrate
celery -A audiencias_publicas beat -l info --pidfile="" --scheduler django_celery_beat.schedulers:DatabaseScheduler