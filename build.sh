#!/usr/bin/env bash
set -o errexit

# Make sure DJANGO_SETTINGS_MODULE is set
export DJANGO_SETTINGS_MODULE=project.settings

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Create superuser (only if not exists)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin','admin@example.com','admin')" | python manage.py shell

