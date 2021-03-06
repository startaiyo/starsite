
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
from django.contrib.auth.models import User
@sched.scheduled_job('cron', hour=0)
def scheduled_job():
    people=User.objects.all()
    for human in people:
        work=Work.objects.filter(create_user=human).all()
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
        if len(contentlist)>0:
            message = 'おはようございます。本日は'+'・'.join(contentlist)+'予定があります。'
        else:
            message = 'おはようございます。本日の予定はありません。'
        from_mail = settings.DEFAULT_FROM_EMAIL
        recipient = [human.email]
        send_mail(subject, message, from_mail, recipient)

@sched.scheduled_job('interval', hours=1)
def timed_job():
    people=User.objects.all()
    for human in people:
        work=Work.objects.filter(create_user=human).all()
        contentlist=[]
        for item in work:
            if item.day == datetime.date.today().weekday():
                contentlist.append(item.content)
            elif item.date == datetime.date.today().day:
                contentlist.append(item.content)
            elif item.interval !=0:
                if (datetime.date.today()-item.created_at.date()).days % item.interval==0:
                    contentlist.append(item.content)
        print (human.email)
        if len(contentlist)>0:
            message = 'おはようございます。本日は'+'・'.join(contentlist)+'予定があります。'
        else:
            message = 'おはようございます。本日の予定はありません。'
        print (contentlist)
        print(message)

sched.start()