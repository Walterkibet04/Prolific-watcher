from django.contrib import admin

# Register your models here.
from .models import SeenStudy

@admin.register(SeenStudy)
class SeenStudyAdmin(admin.ModelAdmin):
    list_display = ("study_id", "name", "reward", "estimated_time", "detected_at")
    readonly_fields = ("detected_at",)