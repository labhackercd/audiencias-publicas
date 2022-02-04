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

python3 manage.py migrate
python3 create_admin.py
python3 manage.py compress --force
python3 manage.py collectstatic --no-input

crontab /etc/cron.d/audiencias
crond

exec daphne -b 0.0.0.0 -p 8000 audiencias_publicas.asgi:application