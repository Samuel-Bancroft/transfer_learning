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
    path('how-to/how-to-create-model/', views.how_to_create_model),
    path('how-to/how-to-sort-model/', views.how_to_sort_model),
    path('how-to/how-to-plot-data/', views.how_to_plot_data),
    path('how-to/how-to-train-model/', views.how_to_train_model),
    path('create-model/dataset_type/', views.dataset_type_choice),
    path('create-model/dataset_type/img-dataset/', views.img_dataset_type),
    path('create-model/dataset_type/num-dataset/', views.num_dataset_type),
    path(r'model_test/', views.model_test),
    path('sort_data/', views.sort_data, name='sort_data'),
    path(r'plot_data', views.plot_data, name='plot_data'),
    path('contact-us/', views.contact_us),
    path('details/<int:id>', views.details, name='details'),
    path('sorted_details/<int:id>', views.sorted_details, name='sorted_details'),
    path('image_details/<int:id>', views.image_model_details, name='image_model_details'),
    path('training/', views.training, name='training'),
    path('user_edited_training/', views.training_including_user_params, name='user_edited_training'),
]