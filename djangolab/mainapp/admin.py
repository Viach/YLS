from django.contrib import admin
from mainapp.models import Lab


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'json_field']
