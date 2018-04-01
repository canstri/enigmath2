from django.contrib import admin

# Register your models here.
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "content_object", "timestamp" ]
    list_display_links = ["user"]
    list_filter = ["user"]

    search_fields = ["user", "content_object"]
    class Meta:
        model = Comment


admin.site.register(Comment, CommentModelAdmin)