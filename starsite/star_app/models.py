from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
import datetime
from datetime import timezone

# Create your models here.
class Work(models.Model):
    content=models.TextField('習慣にしたいこと')
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
    day=models.IntegerField('曜日',null=True,default=None,choices=DAY,validators=[MinValueValidator(0)])
    date=models.IntegerField('毎月○日',validators=[MinValueValidator(0),MaxValueValidator(31)],default=0)
    interval=models.IntegerField('○日間隔',validators=[MinValueValidator(0)],default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    create_user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def get_delta(self):
        today = datetime.datetime.now(timezone.utc) 
        dt=(today-self.created_at).days
        return dt

class Meal(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True)
    calcium = models.CharField(max_length=100)
    calorie = models.CharField(max_length=100)
    carbohydrate = models.CharField(max_length=100)
    dietary_fiber = models.CharField(max_length=100)
    fat = models.CharField(max_length=100)
    food_id = models.CharField(max_length=100)
    food_name = models.CharField(max_length=300)
    potassium = models.CharField(max_length=100)
    protein = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    sodium = models.CharField(max_length=100)
    vitamin_a = models.CharField(max_length=100)
    vitamin_c = models.CharField(max_length=100)
    vitamin_d = models.CharField(max_length=100)
    vitamin_e = models.CharField(max_length=100)
    vitamin_k = models.CharField(max_length=100)