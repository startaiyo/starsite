
from django.conf import settings
from django.core.mail import send_mail
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starsite.settings')

import django 
django.setup()
from star_app.models import Work 
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=30)
def scheduled_job():
    work=Work.objects.get(day=1)
    wk=work.content
    subject = 'Djangoアプリから通知'
    massege = 'おはようございます。本日は{0}の予定があります。'.format(wk)
    from_mail = settings.DEFAULT_FROM_EMAIL
    recipient = ["startaiyo0104@gmail.com"]
    send_mail(subject, massege, from_mail, recipient)

@sched.scheduled_job('interval', minutes=30)
def timed_job():
    print('This job is run every thirty seconds.')

sched.start()