from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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