#!/bin/bash

postgres_ready(){
python3 << END
import sys
import psycopg2
from os import environ

dbname = environ['DATABASE_NAME']
user = environ['DATABASE_USER']
password = environ['DATABASE_PASSWORD']
host = environ['DATABASE_HOST']

try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable. Waiting."
  sleep 1
done


python3 manage.py migrate
python3 create_admin.py
python3 manage.py compress --force
python3 manage.py collectstatic --no-input

crontab /etc/cron.d/audiencias
crond

exec daphne -b 0.0.0.0 -p 8000 audiencias_publicas.asgi:channel_layer
