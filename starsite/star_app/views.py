from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail 

# Create your views here.
def index(request):
    return render(request,'star_app/index.html')

def alert(request):
    return render(request,'star_app/alert.html')

def register(request):
    subject = 'Djangoアプリから通知'
    massege = 'おはようございます。本日はhogehogeの予定があります。'
    from_mail = settings.DEFAULT_FROM_EMAIL
    recipient = ["startaiyo0104@gmail.com"]
    send_mail(subject, massege, from_mail, recipient)
    return render(request,'star_app/alert.html')