from django.urls import path, include
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.home),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', views.register),
    path('users/', views.user),
    path('about_page/', views.about_page),
    path('how-to/', views.how_to),
    path('create-model/', views.upload_file),
    path(r'model_test/', views.model_test),
    path(r'sort_data/', views.sort_data, name='sort_data'),
    path(r'plot_data', views.plot_data, name='plot_data'),
    path('contact-us/', views.contact_us),
    path('details/<int:id>', views.details, name='details'),
]