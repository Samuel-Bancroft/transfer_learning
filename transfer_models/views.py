from django.shortcuts import render, reverse, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from .forms import *
from .models import *
#from .update_data import updates
from .functions import get_columns, get_count
import logging

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

logger = logging.getLogger(__name__)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            template = loader.get_template('home.html')
            return HttpResponse(template.render())
    else:
        template = loader.get_template('login.html')
        return HttpResponse(template.render())


def register(request):
    if request.method == 'POST':
        form = AddMemberForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data('username')
            if not Member.objects.filter(username=username).first():
                password = form.cleaned_data('password')
                email = form.cleaned_data('email')
                firstname = form.cleaned_data('firstname')
                lastname = form.cleaned_data('lastname')
                form = Member(username=username,
                              password=password,
                              firstname=firstname,
                              lastname=lastname,
                              email=email)
                form.save()
                user = Member.objects.filter(username=username, password=password).first()
                context = {'user': form, "user_created": True}
            else:
                context = {'error': 'User already registered, please try again'}
                template = loader.get_template('register.html')
                return HttpResponse(template.render(context))
def logout(request):
    logout(request)
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    else:
        template = loader.get_template('home.html')
        models = CreateModel.objects.filter(created_by=request.user.username)
        context = {'models': models}
        return HttpResponse(template.render(context))

def about_page(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def how_to(request):
    template = loader.get_template('how-to.html')
    return HttpResponse(template.render())

def contact_us(request):
    template = loader.get_template('contact-page.html')
    return HttpResponse(template.render())

def user(request):
    template = loader.get_template('user-page.html')
    return HttpResponse(template.render())

def model_test(request):
    if request.method == 'POST':
        template = loader.get_template('data_test.html')
        model = CreateModel.objects.filter().order_by('date_created').first()

        context = {'obj': model}
        return redirect('create-model/model_test/data-test' ,context)
    else:
        return render(request, 'model_test.html')

def create_model(request):
    template = loader.get_template('user-page.html')
    return HttpResponse(template.render())


def sort_data(request):
    context = {'obj': 'string'}
    return redirect('sort_data' , context)

def plot_data(request):
    template = loader.get_template('plot-data.html')
    obj = CreateModel.objects.filter().order_by('date_created').first()
    context = {'columns': obj.column_name_list}
    if request.method =='POST':
        x = request.POST.get('column_x')
        y = request.POST.get('column_y')
        plot_type = request.POST.get('plot_type')
        file = obj.file
        df = pd.read_csv(file)
        xpoints = df[[str(request.POST.get('column_x'))]]
        ypoints = df[[str(request.POST.get('column_y'))]]
        fig = plt.figure()
        if plot_type == 'line_plot':
            plt.plot(xpoints, ypoints)
        elif plot_type == 'scatter_plot':
            plt.scatter(xpoints, ypoints)
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        context = {'columns': obj.column_name_list,'plot_display': True if x else False, 'plot': data, 'obj': obj}
        return HttpResponse(template.render(context, request))
    else:
        context = {'columns': obj.column_name_list}
        return HttpResponse(template.render(context, request))

def upload_file(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    else:
        if request.method == 'POST':
            form = CreateModelForm(request.POST, request.FILES)
            if form.is_valid():
                template = loader.get_template('model_test.html')
                model_name = form.cleaned_data['model_name']
                files = form.cleaned_data['file']
                username = request.user.username
                created_by = Member.objects.get(firstname=username)
                columns = get_columns(files)
                file_type = form.cleaned_data['file_type']
                file_data_type = form.cleaned_data['file_data_type']
                form = CreateModel(model_name=model_name,
                                                    file=files,
                                                    created_by=created_by,
                                                    columns=columns,
                                                    file_data_type=file_data_type,
                                                    file_type=file_type
                                                )
                form.save()
                columns_list = columns.split(',')
                context = {'obj': form,'proceed': True if form else False,'column_count': get_count(columns), 'columns_list': columns_list}
                return HttpResponse(template.render(context, request))
        else:
            form = CreateModelForm()
            return render(request, 'user-page.html', {'form': form})

def get_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            #form.save()
            #return HttpResponseRedirect("contact-us/thank-you/")
            return HttpResponseRedirect("/thank-you/")
    else:
        form = ContactForm()
    return render(request, "contact-page.html", {"form": form})