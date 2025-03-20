from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # path('', views.event_list, name='event_list'),
    path('', views.EventListAPIView.as_view(), name='event_list'),
    # path('create/', views.create_event, name='create_list'),
    path('create/', views.EventCreateAPIView.as_view(), name='create_list'),
    # path('event/delete/<int:pk>/', views.delete_event, name='delete_list'),
    path('event/delete/<int:pk>/', views.EventDeleteAPIView.as_view(), name='delete_list'),
    # path('event/update/<int:pk>/', views.update_event, name='update_list'),
    path('event/update/<int:pk>/', views.EventUpdateAPIView.as_view(), name='update_list'),
]