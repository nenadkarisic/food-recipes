#!/bin/bash
set -e  # Stop on error

./wait_for_postgres.sh postgres

# Django setup commands
python manage.py makemigrations
python manage.py migrate
python manage.py idempotent_createsuperuser --no-input \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" \
    --first_name "$DJANGO_SUPERUSER_FIRST_NAME" \
    --last_name "$DJANGO_SUPERUSER_LAST_NAME"

# Start the Django application
python manage.py runserver 0.0.0.0:8000