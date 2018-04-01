from django.contrib import admin

# Register your models here.
from .models import Problem, CheckProblem, Lemma

class ProblemModelAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "id", "content_type", "object_id"]
    list_display_links = ["title"]

    search_fields = ["title", "content_object"]
    class Meta:
        model = Problem

class CheckProblemModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "problem_id", "solved"]
    list_display_links = ["id"]
    list_filter = ["user", "problem_id", "solved"]

    search_fields = ["user", "problem_id"]
    class Meta:
        model = CheckProblem

class LemmaModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]  
    class Meta:
        model = Lemma



admin.site.register(Problem, ProblemModelAdmin)

admin.site.register(CheckProblem, CheckProblemModelAdmin)

admin.site.register(Lemma, LemmaModelAdmin)