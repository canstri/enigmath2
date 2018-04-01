from django import forms
from pagedown.widgets import PagedownWidget
from .models import Olymp
from django.forms import CharField


class OlympForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    start_time = forms.DateField(widget=forms.SelectDateWidget)
    
    class Meta:
        model = Olymp
        fields = [
            "title",
            "image",
            "draft",
            "start_time",   
            "publish",
        ]