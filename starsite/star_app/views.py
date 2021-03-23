from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request,'star_app/index.html')

def alert(request):
    return render(request,'star_app/alert.html')

def register(request):
    return render(request,'star_app/index.html')