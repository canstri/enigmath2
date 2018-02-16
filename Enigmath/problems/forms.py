from django import forms

from .models import Problem
from django.forms import CharField


class CreateProblemForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label='', widget=forms.Textarea)
    class Meta:
        model = Problem
        fields = [
            "title",
            "content",
        ]