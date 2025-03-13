from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_list'),
    path('event/delete/<int:pk>/', views.delete_event, name='delete_list'),
    path('event/update/<int:pk>/', views.update_event, name='update_list'),
]