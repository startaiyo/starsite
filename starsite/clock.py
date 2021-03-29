
from django.conf import settings
from django.core.mail import send_mail
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starsite.settings')

import django 
django.setup()
from star_app.models import Work 
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
import datetime
@sched.scheduled_job('interval', minutes=30)
def scheduled_job():
    work=Work.objects.all()
    contentlist=[]
    for item in work:
        if item.day == datetime.date.today().weekday():
            contentlist.append(item.content)
        elif item.date == datetime.date.today().day:
            contentlist.append(item.content)
        elif item.interval !=0:
            if (datetime.date.today()-item.created_at.date()).days % item.interval==0:
                contentlist.append(item.content)
    subject = 'bohlappから通知'
    massege = 'おはようございます。本日は'+'・'.join(contentlist)+'予定があります。'
    from_mail = settings.DEFAULT_FROM_EMAIL
    recipient = ["startaiyo0104@gmail.com"]
    send_mail(subject, massege, from_mail, recipient)

@sched.scheduled_job('interval', minutes=10)
def timed_job():
    work=Work.objects.all()
    contentlist=[]
    for item in work:
        if item.day == datetime.date.today().weekday():
            contentlist.append(item.content)
        elif item.date == datetime.date.today().day:
            contentlist.append(item.content)
        elif item.interval !=0:
            if (datetime.date.today()-item.created_at.date()).days % item.interval==0:
                contentlist.append(item.content)
    print('おはようございます。本日は'+'・'.join(contentlist)+'予定があります。')
    

sched.start()