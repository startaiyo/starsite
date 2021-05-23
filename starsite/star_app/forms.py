from django import forms
from .models import Work, Meal, BodyWeight, UserInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class WorkModelForm(forms.ModelForm):
    class Meta:
        model=Work
        exclude=['create_user']
        widgets = { 
            'content':forms.Textarea(attrs={'rows':4,'cols':30}),
        }

class UserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=("username","email")

class MealModelForm(forms.ModelForm):
    class Meta:
        model=Meal
        fields=['weight']

class WeightModelForm(forms.ModelForm):
    class Meta:
        model=BodyWeight
        fields=['weight']

class UserInfoModelForm(forms.ModelForm):
    class Meta:
        model=UserInfo
        fields=('age','gender')