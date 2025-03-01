from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password-change/', views.change_password, name='password_change'),
    path('password_reset/', views.reset_password_request, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
]