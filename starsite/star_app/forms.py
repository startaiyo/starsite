from django import forms
from .models import Work
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

    