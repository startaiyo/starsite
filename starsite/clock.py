from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.mail import send_mail 
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starsite.settings')
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=0.5)
def scheduled_job():
    subject = 'Djangoアプリから通知'
    massege = 'おはようございます。本日はhogehogeの予定があります。'
    from_mail = settings.DEFAULT_FROM_EMAIL
    recipient = ["startaiyo0104@gmail.com"]
    send_mail(subject, massege, from_mail, recipient)

sched.start()