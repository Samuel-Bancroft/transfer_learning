from django.contrib import admin
from .models import *



class DataModelAdmin(admin.ModelAdmin):
    list_display = ("model_name", "file_type", "file_data_type", "date_created")

class SortedDataModelAdmin(admin.ModelAdmin):
    list_display = ("model_name", "file_type", "file_data_type", "date_created")

# Register your models here.
admin.site.register(DataModel, DataModelAdmin)
admin.site.register(SortedDataModel, SortedDataModelAdmin)

