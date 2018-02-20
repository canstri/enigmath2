from django.contrib import admin

# Register your models here.
from .models import Course

class CourseModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "level"]
    list_display_links = ["title"]
    list_filter = ["title", "level"]

    search_fields = ["content"]
    class Meta:
        model = Course


admin.site.register(Course, CourseModelAdmin)