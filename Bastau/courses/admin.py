from django.contrib import admin

# Register your models here.
from .models import Course
from .models import PassCourse

class CourseModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "level"]
    list_display_links = ["title"]
    list_filter = ["title", "level"]

    search_fields = ["content"]
    class Meta:
        model = Course

class PassCourseModelAdmin(admin.ModelAdmin):
    list_display = ["id",'course_id', 'user', 'passed']
    list_display_links = ["id"]
    list_filter = ["user", "course_id", "passed"]

    search_fields = ["user", "course_id"]
    class Meta:
        model = PassCourse


admin.site.register(Course, CourseModelAdmin)
admin.site.register(PassCourse, PassCourseModelAdmin)