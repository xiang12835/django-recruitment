from __future__ import absolute_import, unicode_literals

from celery import shared_task 
from libs.bot import dingtalk

@shared_task
def send_dingtalk_message(message):
    dingtalk.send(message)