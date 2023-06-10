from django.shortcuts import render, reverse, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
from .forms import *
from .models import *
#from .update_data import updates
from .functions import get_columns, get_count
import matplotlib
import logging
from django.views.decorators.csrf import requires_csrf_token
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from pandas.api.types import is_numeric_dtype
import tensorflow as tf

logger = logging.getLogger(__name__)

def login(request):
    user = ''
    if request.method == 'POST':
        form = LoginAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                template = loader.get_template('home.html')
                return HttpResponse(template.render({'loged_in': True}, request))
        else:
            form = LoginAuthenticationForm()

    return render(request, 'registration/login.html', {'user', user})


def register(request):
    if request.method == 'POST':
        context = {'error': 'User already registered, please try again'}
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context))


def logout(request):
    logout(request)
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def home(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    elif request.user:
        template = loader.get_template('home.html')
        models = CreateModel.objects.filter(created_by__username=request.user.username)
        if models:
            models.order_by('-date_created__history_timestamp')
        sorted_models = SortedModel.objects.filter(created_by__username=request.user.username)
        if sorted_models:
            sorted_models.order_by('date_created__history_timestamp')
        context = {
            'models': models,
            'sorted_models': sorted_models,
            'display_models': True if models else False,
            'display_sorted_models': True if sorted_models else False
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())
    
def about_page(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def how_to(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    template = loader.get_template('how-to.html')
    return HttpResponse(template.render())

def contact_us(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    template = loader.get_template('contact-page.html')
    return HttpResponse(template.render())

def user(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    template = loader.get_template('user-page.html')
    return HttpResponse(template.render())

def model_test(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    if request.method == 'POST':
        template = loader.get_template('data_test.html')
        id = request.session.get('data_id')
        data = CreateModel.objects.get(id=id, created_by__username=request.user.username)
        context = {'obj': data}
        return redirect('create-model/model_test/data-test', context)
    else:
        return render(request, 'model_test.html')

def details(request, id):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    data = CreateModel.objects.get(id=id, created_by__username=request.user.username)
    template = loader.get_template('details.html')
    context = {
        'data': data,
      }
    request.session['data_id'] = data.id
    return HttpResponse(template.render(context, request))

def sorted_details(request, id):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    data = SortedModel.objects.get(id=id, created_by__username=request.user.username)
    template = loader.get_template('sorted_details.html')
    context = {
        'data': data,
      }
    request.session['sorted_data_id'] = data.id
    return HttpResponse(template.render(context, request))

def plot_data(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    data = None
    if request.method == 'GET':
        id = request.session.get('data_id')
        data = CreateModel.objects.get(id=id, created_by__username=request.user.username)
    template = loader.get_template('plot-data.html')
    if not data:
        data = CreateModel.objects.filter(created_by__username=request.user.username).order_by('date_created').first()
    context = {'columns': data.column_name_list}
    matplotlib.use('SVG')
    if request.method =='POST':
        x = request.POST.get('column_x')
        y = request.POST.get('column_y')
        plot_type = request.POST.get('plot_type')
        file = data.file
        df = pd.read_csv(file)
        xpoints = df[[str(x)]]
        ypoints = df[[str(y)]]
        fig = plt.figure()
        if plot_type == 'line_plot':
            plt.plot(xpoints, ypoints)
        elif plot_type == 'scatter_plot':
            plt.scatter(xpoints, ypoints)
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        plot_data = imgdata.getvalue()
        context = {'columns': data.column_name_list,'plot_display': True if x else False, 'plot_data': plot_data, 'obj': data}
        return HttpResponse(template.render(context, request))
    else:
        context = {'columns': data.column_name_list}
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
                username = request.user.get_username()
                created_by = User.objects.get(username=username)
                columns = get_columns(files)
                file_type = form.cleaned_data['file_type'] # need to creat function to find the file type
                file_data_type = form.cleaned_data['file_data_type']# need to creat function to find the file data type
                form = CreateModel(model_name=model_name,
                                                    file=files,
                                                    created_by=created_by,
                                                    columns=columns,
                                                    file_data_type=file_data_type,
                                                    file_type=file_type
                                                )
                form.save()
                columns_list = columns.split(',')
                request.session['data_id'] = form.id
                context = {'obj': form,'proceed': True if form else False,'column_count': get_count(columns), 'columns_list': columns_list}
                return HttpResponse(template.render(context, request))
        else:
            form = CreateModelForm()
            return render(request, 'user-page.html', {'form': form})

def sort_data(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    user = request.user.username
    id = request.session.get('data_id')
    data = CreateModel.objects.get(id=id, created_by__username=user)
    if SortedModel.objects.filter(from_file__id=data.id):
        context = {'error': 'Sorted File already exists'}
        template = loader.get_template('sorting-data.html')
        return HttpResponse(template.render(context, request))
    not_sort_data = pd.read_csv(data.file)
    #While this is local storage
    name = f'sorted_{data.file}'
    not_sort_data.to_csv('prep-sort')
    sort_data = pd.read_csv(r'C:\Users\samue\Documents\Transfer_Learning\transfer_learning\{}'.format(name))

    if not data:
        context = {'error': 'No data to work with'}
        template = loader.get_template('sorting-data.html')
        return HttpResponse(template.render(context, request))
    elif sort_data.isnull().values.ravel().sum() > 0:
        #add dropped columsn in to the remoevd_columns list as they have been removed
        sort_data = sort_data.dropna()
    columns = sort_data.columns.values.tolist()
    converted_columns = []
    removed_columns = []
    for column in columns:
        if not is_numeric_dtype(sort_data[column]):
            unique_values = sort_data[column].unique()
            for index, word in enumerate(unique_values):
                converted_columns.append(column)
                sort_data[column] = sort_data[column].replace([word], index)
            if not is_numeric_dtype((sort_data[column])):
                removed_columns.append(column)
                sort_data = sort_data.drop(columns=column)
    sort_data.to_csv(name)
    username = request.user.get_username()
    created_by = User.objects.get(username=username)
    for column in converted_columns[:]:
        if column in removed_columns:
            converted_columns.remove(column)
    converted_columns = ','.join(list(dict.fromkeys(converted_columns)))
    removed_columns = ','.join(list(dict.fromkeys(removed_columns)))
    sorted_model = SortedModel(
        model_name=data.model_name,
        sorted_file= sort_data,
        created_by=created_by,
        columns=','.join(columns),
        file_data_type='numerical',
        file_type=data.file_type,
        from_file=data,
        converted_columns=converted_columns,
        removed_columns=removed_columns
    )
    sorted_model.save()
    context = {'obj': sorted_model,
               'removed_columns': removed_columns.split(","),
               'converted_columns': converted_columns.split(",")
               }
    request.session['sorted_data_id'] = sorted_model.id
    template = loader.get_template('sorting-data.html')
    return HttpResponse(template.render(context, request))

def get_contact(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            #form.save()
            #return HttpResponseRedirect("contact-us/thank-you/")
            return HttpResponseRedirect("/thank-you/")
    else:
        form = ContactForm()
    return render(request, "contact-page.html", {"form": form})

def training(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    user = request.user.username
    id = request.session.get('sorted_data_id')
    sorted_data = SortedModel.objects.filter(id=id, created_by__username=user)
    if not sorted_data:
        context = {'error': 'Sorted File doesnt exist'}
        template = loader.get_template('training.html')
        return HttpResponse(template.render(context, request))
    file = sorted_data.file
    df = pd.read_csv(file)
    target = sorted_data.columns[0]
    features = df[target]
    tf.convert_to_tensor(features)
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(features)
    normalizer(features.iloc[:3])
    SHUFFLE_BUFFER = 500
    BATCH_SIZE = 2

    model = tf.keras.Sequential([
            normalizer,
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(10, activation='relu')
        ])

    model.compile(optimizer='adam',
                      loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])

    model = get_basic_model()
    model.fit(features, target, epochs=15, batch_size=BATCH_SIZE)




