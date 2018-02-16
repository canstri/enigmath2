from django.contrib import admin

from .models import Profile


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "rating", "school" ]
    list_display_links = ["user"]
    list_editable = ["rating"]
    list_filter = ["school"]

    search_fields = ["user", "school"]
    class Meta:
        model = Profile


admin.site.register(Profile, ProfileModelAdmin)