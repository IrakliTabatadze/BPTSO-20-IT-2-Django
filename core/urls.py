from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/add/', views.add_event, name='add_event'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('event/change/<int:pk>/', views.change_event, name='change_event'),
]