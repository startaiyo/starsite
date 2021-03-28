from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Work(models.Model):
    content=models.TextField('習慣にしたいこと')
    DAY=(
        (0, '日'),
        (1, '月'),
        (2, '火'),
        (3, '水'),
        (4, '木'),
        (5, '金'),
        (6, '土'),
    )
    day=models.IntegerField('曜日',null=True,default=None,choices=DAY,validators=[MinValueValidator(1)])
    date=models.IntegerField('毎月○日',validators=[MinValueValidator(1),MaxValueValidator(31)])
    interval=models.IntegerField('○日間隔',validators=[MinValueValidator(1)])
