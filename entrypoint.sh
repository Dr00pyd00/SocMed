#!/usr/bin/env bash
set -e

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput --upload-unhashed-files

echo ">>> Applying migrations..."
python manage.py migrate --noinput

echo ">>> Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
