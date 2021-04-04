from django import template
import datetime
from datetime import timezone

register=template.Library()

@register.filter
def delta(num,dt):
    td = datetime.datetime.now(timezone.utc).day
    delta = num - td - dt
    return delta
    
@register.filter
def modulo(num1,num2):
    if num2 != 0:
        if num1 % num2 == 0:
            return True        