from django import forms
from .models import Problem


class AddProblemForm(forms.ModelForm):
    prblm_id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Problem
        fields = [
            "prblm_id",
        ]