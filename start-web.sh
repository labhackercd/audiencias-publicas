#!/bin/bash

python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 create_admin.py

crontab /etc/cron.d/audiencias
crond

exec daphne -b 0.0.0.0 -p 8000 audiencias_publicas.asgi:channel_layer