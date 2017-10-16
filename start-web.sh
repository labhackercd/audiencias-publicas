#!/bin/bash

python3 manage.py migrate
python3 create_admin.py

exec daphne -b 0.0.0.0 -p 8000 audiencias_publicas.asgi:channel_layer