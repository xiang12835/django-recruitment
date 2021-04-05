# https://docs.celeryproject.org/en/stable/userguide/monitoring.html
celery -A tasks flower --broker=redis://@localhost:6379/0