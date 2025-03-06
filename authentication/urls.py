from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # path('registration/', views.register_user, name='registration'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    # path('login/', views.login_user, name='login'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('password-change/', views.change_password, name='password_change'),
    path('password_reset/', views.reset_password_request, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
]