import pandas as pd
from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class BaseModel(models.Model):
  model_name = models.CharField(max_length=100, default='Default')
  date_created = models.DateField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, default='')
  file_type = models.CharField(max_length=10, default=None)
  file_data_type = models.CharField(max_length=20, default=None)
  class Meta:
    abstract=True


class CreateModel(BaseModel):
  file = models.FileField()
  columns = models.CharField(max_length=1000, default='default')
  class Meta:
    verbose_name_plural = 'Created Models'
    ordering = ('-date_created',)
  def __str__(self):
    return f"{self.model_name}"
  def column_name_list(self):
    return self.columns.split(",")


class SortedModel(BaseModel):
  sorted_data = models.JSONField()
  columns = models.CharField(max_length=1000, default=None)
  from_file = models.OneToOneField(CreateModel, on_delete=models.CASCADE, default='')
  converted_columns = models.CharField(max_length=1000, default=None)
  removed_columns = models.CharField(max_length=1000, default=None)
  def __str__(self):
    return f"{self.model_name} created from {self.from_file.model_name}"

  @classmethod
  def put_dataframe(cls, df):
    store_df = cls(data=df.to_json(orient='split'))
    store_df.save()
    return store_df

  def load_df(self):
    return pd.read_json(self.sorted_data, orient='split')


