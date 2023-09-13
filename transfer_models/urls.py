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
    path('create-model/dataset_type/', views.dataset_type_choice),
    path('create-model/dataset_type/img-dataset/', views.img_dataset_type),
    path('create-model/dataset_type/num-dataset/', views.num_dataset_type),
    path(r'model_test/', views.model_test),
    path('sort_data/', views.sort_data, name='sort_data'),
    path(r'plot_data', views.plot_data, name='plot_data'),
    path('contact-us/', views.contact_us),
    path('details/<int:id>', views.details, name='details'),
    path('sorted_details/<int:id>', views.sorted_details, name='sorted_details'),
    path('training/', views.training, name='training'),
    path('user-edited-training/', views.training_including_user_params, name='user-edited-training'),
]