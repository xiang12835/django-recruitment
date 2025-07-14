from __future__ import absolute_import, unicode_literals

import os, json

from celery import Celery, shared_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

app = Celery('recruitment')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# 方法一：admin后台

# 方法二：直接设置应用的 beat_schedule
from celery.schedules import crontab

# this is important to load the celery tasks
from recruitment.tasks import add

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'recruitment.tasks.add',
        'schedule': 10.0,
        'args': (16, 4, )
    },
}


# 方法三：系统启动时自动注册定时任务
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='hello every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


# 方法四：运行时添加定时任务
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# 示例：创建一个每10分钟执行的任务‌
# 先创建定时策略
schedule, _ = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.MINUTES
)
# 在创建任务
PeriodicTask.objects.create(
    interval=schedule,
    name='Dynamic Task Demo',
    task='recruitment.celery.test',
    args=json.dumps(['welcome']),
)


@app.task
def test(arg):
    print(arg)


app.conf.timezone = "Asia/Shanghai"