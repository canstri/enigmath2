from django.contrib import admin

# Register your models here.
from .models import Lecture

class LectureModelAdmin(admin.ModelAdmin):
    list_display = ["title"]

    search_fields = ["title", "content"]
    class Meta:
        model = Lecture


admin.site.register(Lecture, LectureModelAdmin)