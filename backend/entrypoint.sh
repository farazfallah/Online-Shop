#!/bin/bash

echo "Waiting for redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis started"

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

exec "$@"