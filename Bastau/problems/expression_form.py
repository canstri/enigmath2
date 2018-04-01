from django import forms

from .models import CheckProblem
from django.forms import CharField


class ExpressionForm(forms.ModelForm):
    exp_id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = CheckProblem
        fields = [
            'exp_id',
        ]