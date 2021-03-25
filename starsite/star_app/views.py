from django.shortcuts import render
from . import forms
from star_app.models import Work

# Create your views here.
def index(request):
    return render(request,'star_app/index.html')

def alert(request):
    return render(request,'star_app/alert.html')

def register(request):
    form = forms.WorkModelForm()
    if request.method=='POST':
        form=forms.WorkModelForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'star_app/index.html',context={'form':form})

def all_delete(request):
    work=Work.objects.all()
    work.delete()
    return render(request,'star_app/deleted.html')