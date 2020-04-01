from django import forms
from .models import url_request

class search_form(forms.ModelForm):
    class Meta:
        model= url_request
        fields = ['country']
