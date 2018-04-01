from django.contrib import admin

# Register your models here.
from .models import Lecture, PassLecture

class LectureModelAdmin(admin.ModelAdmin):
    list_display = ["title"]

    search_fields = ["title", "content"]
    class Meta:
        model = Lecture

class PassLectureModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "lecture_id", "passed"]
    list_display_links = ["id"]
    list_filter = ["user", "lecture_id", "passed"]

    search_fields = ["user", "lecture_id"]
    class Meta:
        model = PassLecture

admin.site.register(PassLecture, PassLectureModelAdmin)

admin.site.register(Lecture, LectureModelAdmin)