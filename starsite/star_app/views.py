from django.shortcuts import render, redirect
from . import forms
from star_app.models import Work
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView # 追記
from .forms import UserCreationForm  # 追記
from django.urls import reverse_lazy
from django.http import Http404
import datetime
import calendar
from datetime import timezone
from star_app.models import Work 
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "star_app/create.html"
    success_url = reverse_lazy("login")

@login_required
def index(request):
    work=Work.objects.filter(create_user=request.user).all()
    if len(work)!=0:
        work=work
    else:
        work=None
    today = datetime.datetime.now(timezone.utc) 
    cal = calendar.Calendar(firstweekday=0) 
    this_month_cal = cal.itermonthdays2(today.year,today.month)
    this_month = today.month
    this_year = today.year
    this_day = today.day
    return render(request,'star_app/index.html',context={'work':work,'this_day':this_day,'this_year':this_year,'this_month':this_month, 'this_month_cal':this_month_cal})

@login_required
def alert(request):
    work=Work.objects.filter(create_user=request.user).all()
    if len(work)!=0:
        work=work
    else:
        work=None
    
    DAY=(
        (7, '未選択'),
        (6, '日'),
        (0, '月'),
        (1, '火'),
        (2, '水'),
        (3, '木'),
        (4, '金'),
        (5, '土')
    )
    return render(request,'star_app/alert.html',{'work':work, 'DAY':DAY})

def register(request):
    form = forms.WorkModelForm()
    if request.method=='POST':
        form=forms.WorkModelForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.create_user=request.user
            post.save()
            return redirect('index')
    else:
        form=forms.WorkModelForm()

    return render(request,'star_app/register.html',context={'form':form})

def top(request):
    return render(request,'star_app/top.html')

def delete(request,id):
    try:
        work=Work.objects.get(id=id)
    except Work.DoesNotExist:
        raise Http404
    work.delete()
    return redirect('alert')

def all_delete(request):
    work=Work.objects.all()
    work.delete()
    return render(request,'star_app/deleted.html')

def lunchmap(request):
    context={'api_key':settings.GOOGLE_MAP_API_KEY}
    return render(request,'star_app/lunchmap.html',context)