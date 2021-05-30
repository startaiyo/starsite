from django.shortcuts import render, redirect
from . import forms
from star_app.models import Work, Meal, BodyWeight, UserInfo
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView # 追記
from .forms import UserCreationForm  # 追記
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
import datetime
import calendar
from datetime import timezone
from star_app.models import Work 
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
import io
import matplotlib
# バックエンドにAggを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from django import utils
import json
from .idealnutrition import idealnut
import copy
# Create your views here.
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "star_app/create.html"
    success_url = reverse_lazy("login")

@login_required
def index(request):
    work = Work.objects.filter(create_user=request.user).all()
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
    work = Work.objects.filter(create_user=request.user).all()
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
        work = Work.objects.get(id=id)
    except Work.DoesNotExist:
        raise Http404
    work.delete()
    return redirect('alert')

def all_delete(request):
    work = Work.objects.all()
    work.delete()
    return render(request,'star_app/deleted.html')

@login_required
def lunchmap(request):
    context={'api_key':settings.GOOGLE_MAP_API_KEY}
    return render(request,'star_app/lunchmap.html',context)

@login_required
def meals(request):
    meal = Meal.objects.filter(user_id=request.user.id).all()
    if len(meal)!=0:
        meal = meal
    else:
        meal = None
    try:
        userinfo = UserInfo.objects.get(user_id=request.user.id)
    except:
        userinfo = None
    mealdata = []
    mealdata2 = []
    # 理想的栄養素をdays日分乗じる
    def ideal(i,ds,md):
        ideal = idealnut[i].copy()
        ideal['data'] = [n*ds for n in idealnut[i]['data']]
        md.append(ideal)

    def get_user_data(ui,md,days):
        if ui:
            if ui.gender == "man":
                if ui.age <= 29:
                    ideal(0,days,md)
                elif ui.age >= 30 and ui.age <= 49:
                    ideal(1,days,md)
                elif ui.age >= 50:
                    ideal(2,days,md)
            elif ui.gender == "woman":
                if ui.age <= 29:
                    ideal(3,days,md)
                elif ui.age >= 30 and ui.age <= 49:
                    ideal(4,days,md)
                elif ui.age >= 50:
                    ideal(5,days,md)
    # レーダーチャートに理想栄養追加
    get_user_data(userinfo,mealdata,7)
    get_user_data(userinfo,mealdata2,1)

    today = datetime.datetime.now(timezone.utc)
    def get_data(ds, ml, md, label):
        start_time = today - datetime.timedelta(days=ds)
        meal=ml.filter(created_at__range=(start_time,today))
        week_protein,week_fat,week_dietary_fiber,week_carbohydrate,week_salt,week_potassium,week_calcium,week_vitamin_a,week_vitamin_c,week_vitamin_e,week_vitamin_k,week_vitamin_d=[],[],[],[],[],[],[],[],[],[],[],[]
        for item in meal:
            week_protein.append(float(item.protein)/10)
            week_fat.append(float(item.fat)/10)
            week_dietary_fiber.append(float(item.dietary_fiber)/3)
            week_carbohydrate.append(float(item.carbohydrate)/100)
            week_salt.append(float(item.salt))
            week_potassium.append(float(item.potassium)/500) 
            week_calcium.append(float(item.calcium)/100)
            week_vitamin_a.append(float(item.vitamin_a)/300)
            week_vitamin_c.append(float(item.vitamin_c)/10)
            week_vitamin_e.append(float(item.vitamin_e))
            week_vitamin_k.append(float(item.vitamin_k)/30)
            week_vitamin_d.append(float(item.vitamin_d))
        
        weekdata = {
            'label':label,
            'data':[round(sum(week_protein),1),round(sum(week_fat),1),round(sum(week_dietary_fiber),1),round(sum(week_carbohydrate),1),round(sum(week_salt),1),round(sum(week_potassium),1),round(sum(week_calcium),1),round(sum(week_vitamin_a),1),round(sum(week_vitamin_c),1),round(sum(week_vitamin_e),1),round(sum(week_vitamin_k),1),round(sum(week_vitamin_d),1)]
        }
        md.append(weekdata)
    # レーダーチャートに実データ追加
    get_data(7, meal, mealdata, 'weekly_data')
    get_data(1, meal, mealdata2, 'daily_data')
    GENDER = (
        ('man','男性'),
        ('woman','女性'),
        ('other','その他')
    )
    return render(request,'star_app/meal.html',context={'meal':meal,'userinfo':userinfo,'mealdata':json.dumps(mealdata),'mealdata2':json.dumps(mealdata2)})

@login_required
def meals_page(request):
    ui = request.user.id
    return redirect(f'https://bohlapp.vercel.app/?user_id={ui}')

@csrf_exempt
def mealsregister(request, *args, **kwargs):
    parameters=urllib.parse.urlparse(request.body)
    mealsdata=urllib.parse.parse_qs(parameters.path.decode('utf-8'))
    for k in mealsdata:
        v1 = mealsdata[k][0]
        mealsdata[k] = v1
    v2 = int(mealsdata['user_id'])
    mealsdata['user_id'] = v2
    print(mealsdata)
    try:
        meal=Meal(**mealsdata)
        meal.save()
        print('success!')
    except:
        print('failed')

def weight(request, id):
    meal = Meal.objects.filter(user_id=request.user.id).all()
    if len(meal)!=0:
        meal = meal
    else:
        meal = None
    mealinfo=Meal.objects.get(id=id)
    w = mealinfo.weight
    form=forms.MealModelForm()
    if request.method=='POST':
        form=forms.MealModelForm(request.POST,instance=mealinfo)
        # g数に応じて各栄養素量変化
        if form.is_valid():
            mealinfo = form.save(commit=False)
            a = round(float(mealinfo.calcium))
            mealinfo.calcium = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.calorie))
            mealinfo.calorie = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.carbohydrate))
            mealinfo.carbohydrate = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.dietary_fiber))
            mealinfo.dietary_fiber = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.fat))
            mealinfo.fat = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.potassium))
            mealinfo.potassium = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.protein))
            mealinfo.protein = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.salt))
            mealinfo.salt = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.sodium))
            mealinfo.sodium = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.vitamin_a))
            mealinfo.vitamin_a = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.vitamin_d))
            mealinfo.vitamin_d = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.vitamin_c))
            mealinfo.vitamin_c = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.vitamin_e))
            mealinfo.vitamin_e = str(round(a*mealinfo.weight/w))
            a = round(float(mealinfo.vitamin_k))
            mealinfo.vitamin_k = str(round(a*mealinfo.weight/w))
            mealinfo.save()
            return redirect('meals')
    return render(request,'star_app/meal.html',context={'form':form,'meal':meal,'mealinfo':mealinfo})

def deletemeal(request,id):
    try:
        meal = Meal.objects.get(id=id)
    except Meal.DoesNotExist:
        raise Http404
    meal.delete()
    return redirect('meals')

def create_graph(x_list,t_list):
#  グラフの初期化
    plt.cla()
    plt.plot(t_list, x_list, label="x")
    plt.xlabel('date')
    plt.ylabel('weight(kg)')

def get_image():
#  バイナリデータをメモリ上に書き出す
    buffer = io.BytesIO()
#  上記のpltをpng形式にして保存
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def bweight(request):
    form = forms.WeightModelForm()
    if request.method=='POST':
        form=forms.WeightModelForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('bweight')
    else:
        form=forms.WeightModelForm()
    bweightinfo=BodyWeight.objects.filter(user_id=request.user.id).all()
    x_list = []
    t_list = []
    for item in bweightinfo:
        t_list.append(item.created_at)
        x_list.append(item.weight)
    create_graph(x_list, t_list)
    graph = get_image()
    return render(request,'star_app/bweight.html',context={'graph':graph,'form':form,'bweightinfo':bweightinfo})

def userinfo(request):
    form=forms.UserInfoModelForm()
    if request.method=='POST':
        form=forms.UserInfoModelForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('meals')
    else:
        form=forms.UserInfoModelForm()
    return render(request,'star_app/user_info.html',context={'form':form})