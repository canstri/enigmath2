from django import forms

from .models import Problem
from django.forms import CharField


class SaveProblemForm(forms.ModelForm):
    expr1 = forms.CharField(label='', widget=forms.Textarea, required=False)
    expr2 = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = Problem
        fields = [
            "expr1",
            "expr2",
        ]