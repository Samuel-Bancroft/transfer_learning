from django.contrib import admin
from .models import *



class CreateModelAdmin(admin.ModelAdmin):
    list_display = ("model_name", "file_type", "file_data_type", "date_created")

class SortedModelAdmin(admin.ModelAdmin):
    list_display = ("model_name", "file_type", "file_data_type", "date_created")

# Register your models here.
admin.site.register(CreateModel, CreateModelAdmin)
admin.site.register(SortedModel, SortedModelAdmin)

