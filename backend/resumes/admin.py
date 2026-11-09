from django.contrib import admin
from .models import CV
@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "language", "template", "updated_at")
    search_fields = ("title", "owner__username")
