from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail 
import schedule, time


# Create your views here.
def index(request):
    return render(request,'star_app/index.html')

def alert(request):
    return render(request,'star_app/alert.html')

def register(request):
    return render(request,'star_app/index.html')