#!/usr/bin/sh
chown -R http /app/src
uwsgi --socket 127.0.0.1:4000 --plugin python -H venv --chdir src --home /app/venv --wsgi-file odapp/wsgi.py --master --processes 4 --threads 2 --uid http &
nginx -g 'daemon off;'