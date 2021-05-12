from django.urls import path
from . import views
urlpatterns = [
    path('',views.top,name ='top'),
    path('index/',views.index,name='index'),
    path('alert/',views.alert,name='alert'),
    path('register/',views.register,name='register'),
    path('all_delete/',views.all_delete,name='all_delete'),
    path('create/', views.UserCreateView.as_view(),name="create"),
    path('delete/<int:id>/', views.delete,name='delete'),
    path('lunchmap/', views.lunchmap,name='lunchplace'),
    path('meals/', views.meals, name='meals'),
    path('meals_page/', views.meals_page, name='meals_page'),
    path('meals/register/', views.mealsregister, name='mealsregister')
]