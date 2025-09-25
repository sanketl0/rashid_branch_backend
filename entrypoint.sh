#!/bin/sh

APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/gunicorn --workers 3 -k eventlet --worker-tmp-dir /dev/shm autocount.wsgi:application --bind "0.0.0.0:${APP_PORT}"