#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Set DJANGO_SETTINGS_MODULE so Django can run
export DJANGO_SETTINGS_MODULE=project.settings  # <-- replace your_project

# Create superuser if it doesn't exist
python - <<END
from django.contrib.auth import get_user_model
import django
django.setup()
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
END
