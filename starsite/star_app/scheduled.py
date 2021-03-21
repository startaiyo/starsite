from apscheduler.schedulers.background import BackgroundScheduler
from .scheduled_mail import scheduled_mail


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_mail, 'interval', seconds=30)
    scheduler.start()