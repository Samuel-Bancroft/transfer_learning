from django import forms
from django.db import models
from .models import *
from django.contrib.auth.models import User


class LoginAuthenticationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=100)

    class Meta:
        model=User
        fields = ['username', 'password']



class CreateModelForm(forms.ModelForm):
    class Meta:
        model = CreateModel
        fields = ["model_name", "file", 'file_type', 'file_data_type']#, 'created_by']
        labels = {"model_name": "Model Name", "file": "File", 'file_type': 'File Type', 'file_data_type':'File Data Type'}#, 'created_by':"Created By"}


class Contact(models.Model):
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  comment = models.EmailField(max_length=1000)

def faq_suggestions(value):
    pass

class ContactForm(forms.ModelForm):
    age = forms.IntegerField()
    comment = forms.CharField(widget=forms.Textarea, validators=[faq_suggestions])
    class Meta:
        model = Contact
        fields = '__all__'

