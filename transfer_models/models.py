import pandas as pd
from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class FileToJSON(models.Model):
  data = models.JSONField()

  @classmethod
  def store_dataframe(cls, df):
    store_data = cls(data=df.to_json(orient='split'))
    store_data.save()
    return store_data

  def load_dataframe(self):
    return pd.read_json(self.data, orient='split')


class BaseDataModel(models.Model):
  file = models.FileField(default='Default', upload_to='files/%Y/%b/%d')
  model_name = models.CharField(max_length=100, default='Default')
  date_created = models.DateField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, default='')
  file_type = models.CharField(max_length=10, default=None)
  file_data_type = models.CharField(max_length=20, default='N/A')
  class Meta:
    abstract=True


class DataModel(BaseDataModel):
  columns = models.CharField(max_length=1000, default='default')
  class Meta:
    verbose_name_plural = 'Data Models'
    ordering = ['-date_created']
  def __str__(self):
    return f"{self.model_name}"
  def column_name_list(self):
    return self.columns.split(",")


class SortedDataModel(BaseDataModel):
  columns = models.CharField(max_length=1000, default=None)
  from_file = models.OneToOneField(DataModel, on_delete=models.CASCADE, default='')
  sorted_file = models.FileField(default=None, upload_to='sorted_files/%Y/%b/%d')
  converted_columns = models.CharField(max_length=1000, default=None)
  removed_columns = models.CharField(max_length=1000, default=None)
  class Meta:
    verbose_name_plural = 'Sorted Data Models'
    ordering = ['-date_created']
  def __str__(self):
    return f"{self.model_name}: Is sorted data from {self.from_file.model_name}"


def user_directory_path(instance, filename):
  # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
  return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)




