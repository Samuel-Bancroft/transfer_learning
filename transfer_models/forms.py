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
        labels = {'username': 'Username', 'password': 'Password'}


class DataModelForm(forms.ModelForm):
    file = forms.FileField(label='File')
    class Meta:
        model = DataModel
        fields = ["model_name", "file", 'file_type', 'file_data_type']
        labels = {"model_name": "Model Name", "file": "File", 'file_type': 'File Type', 'file_data_type':'File Data Type'}


class ImageModelForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['img_name', 'img', 'file_type']
        labels = {"img_name": "Model Name", "img": "Image", 'file_type': 'File Type'}


class DataUserTrainingParams(forms.ModelForm):
    data_feature_removal = forms.CharField(max_length=100)
    hiddenlayer_count = forms.IntegerField(max_value=1000)
    activation_functions = forms.Textarea()
    loss_function = forms.CharField(max_length=100)
    optimization = forms.CharField(max_length=100)
    metrics = forms.CharField(max_length=100)
    epoch = forms.IntegerField(max_value=1000)
    batch_size = forms.IntegerField(max_value=1000)
    random_state = forms.Textarea()
    class Meta:
        fields = [
            'data_feature_removal',
            'activation_functions',
            'loss_function',
            'optimization',
            'metrics',
            'epoch',
            'batch_size',
            'random_state',
            'hiddenlayer_count'
        ]
        labels = {
            'data_feature_removal': 'Data Feature',
            'activation_functions': 'Activation Functions',
            'loss_function': 'Loss Function',
            'optimization': 'Optimization Function',
            'metrics': 'Metrics',
            'epoch': 'Epoch Count',
            'batch_size': 'Batch Size',
            'random_state': 'Random state',
            'hiddenlayer_count': 'Hidden Layer counts'
        }


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


