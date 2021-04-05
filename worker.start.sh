# https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html
DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment worker -l info