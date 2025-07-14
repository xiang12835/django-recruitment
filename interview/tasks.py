from __future__ import absolute_import, unicode_literals

from celery import shared_task 
from libs.bot import dingtalk

# DJANGO_SETTINGS_MODULE=settings.local celery --app recruitment worker -l info

@shared_task
def send_dingtalk_message(message):
    dingtalk.send(message)