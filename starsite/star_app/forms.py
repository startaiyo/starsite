from django import forms
from .models import Work
class WorkModelForm(forms.ModelForm):
    class Meta:
        model=Work
        exclude=['create_user']