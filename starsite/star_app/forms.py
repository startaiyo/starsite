from django import forms
from .models import Work
class WorkModelForm(forms.ModelForm):
    class Meta:
        model=Work
        fields='__all__'