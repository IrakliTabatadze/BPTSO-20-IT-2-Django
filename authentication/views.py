from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

# def register_user(request):
#
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#
#             login(request, form.user)
#
#             return redirect('event_list')
#
#         else:
#             return render(request, 'registration/registration.html', {'form': form})
#
#     else:
#         form = RegistrationForm()
#
#         return render(request, 'registration/registration.html', {'form': form})

class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('authentication:login')


# def login_user(request):
#
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('event_list')
#
#     else:
#         form = AuthenticationForm()
#         return render(request, 'registration/login.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'registration/login.html'

# def logout_user(request):
#     logout(request)
#     return redirect('login')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('core:event_list')



# @login_required(login_url='login')
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#
#             update_session_auth_hash(request, request.user)
#
#             return redirect('event_list')
#
#     else:
#         form = PasswordChangeForm(user=request.user)
#
#         return render(request, 'registration/change_password.html', {'form': form})

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('core:event_list')



# def reset_password_request(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#
#         if form.is_valid():
#             form.save(
#                 request=request,
#                 use_https=False,
#                 email_template_name='registration/password_reset_emai.html',
#             )
#
#             return  HttpResponse('Reset Email Sent, Please Check Your Email To Finish Process')
#
#     else:
#         form = PasswordResetForm()
#         return  render(request, 'registration/password_reset_request.html', {'form': form})


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_request.html'
    email_template_name = 'registration/password_reset_emai.html'
    success_url = reverse_lazy('core:event_list')



# def reset_password_confirm(request, uidb64, token):
#     try:
#         id = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(id=id)
#
#         if default_token_generator.check_token(user, token):
#             if request.method == 'POST':
#                 form = SetPasswordForm(user=user, data=request.POST)
#                 if form.is_valid():
#                     form.save()
#
#                     return redirect('login')
#             else:
#                 form = SetPasswordForm(user=user)
#         else:
#             return  HttpResponse('Invalid Token')
#
#     except (User.DoesNotExist, ValueError):
#         return redirect('/')
#
#     return render(request, 'password_reset_confirm.html', {'form': form})

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('authentication:login')

# API - Application Programming Interface
# RESTFUL API - Representational State Transfer API
# GET, POST, PUT, DELETE