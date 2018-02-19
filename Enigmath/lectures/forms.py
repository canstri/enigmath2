from django import forms
from pagedown.widgets import PagedownWidget
from .models import Lecture
from django.forms import CharField


class LectureForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    title = forms.CharField()
    content = forms.CharField(widget=PagedownWidget(show_preview = False))

    class Meta:
        model = Lecture
        fields = [
            "title",
            "content",
            "level",            
            "draft",
        ]