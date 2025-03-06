from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('', views.event_list, name='event_list'),
    path('', views.EventListView.as_view(), name='event_list'),
    # path('event/add/', views.add_event, name='add_event'),
    path('event/add/', views.CreateEventView.as_view(), name='add_event'),
    # path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    # path('event/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('event/delete/<int:pk>/', views.EventDeleteView.as_view(), name='delete_event'),
    # path('event/change/<int:pk>/', views.change_event, name='change_event'),
    path('event/change/<int:pk>/', views.EventUpdateView.as_view(), name='change_event'),
    path('event/ticket/buy/<int:pk>/', views.buy_ticket, name='buy_ticket'),
]