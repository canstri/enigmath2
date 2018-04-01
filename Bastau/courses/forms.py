from django import forms
from pagedown.widgets import PagedownWidget
from .models import Course
from django.forms import CharField


class CourseForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview = False))
    class Meta:
        model = Course
        fields = [
            "level",
            "title",
            "content",
            "draft",
            "image",
        ]