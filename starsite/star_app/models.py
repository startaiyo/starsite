from django.db import models

# Create your models here.
class Work(models.Model):
    content=models.TextField()
    day=models.IntegerField()
    date=models.DateTimeField()
    interval=models.IntegerField()
