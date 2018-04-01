from django.contrib import admin

# Register your models here.
from .models import Olymp

class OlympModelAdmin(admin.ModelAdmin):
	list_display = ["title", "start_time", "timestamp"]
	list_display_links = ["start_time"]
	list_editable = ["title"]
	list_filter = ["start_time", "timestamp"]

	search_fields = ["title"]
	class Meta:
		model = Olymp


admin.site.register(Olymp, OlympModelAdmin)