from django import forms
from pagedown.widgets import PagedownWidget
from .models import Problem
from django.forms import CharField


class CreateProblemForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=PagedownWidget(show_preview = False))
    class Meta:
        model = Problem
        fields = [
            "title",
            "content",
        ]