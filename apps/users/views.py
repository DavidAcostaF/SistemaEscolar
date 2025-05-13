from django.shortcuts import render
from django.views.generic import View,TemplateView,CreateView
from .models import User
from .forms import RegisterForm,LoginForm
from django.contrib.auth.views import LoginView

# Create your views here.


class UserIndexView(CreateView):
    template_name = 'users/login.html'
    model = User


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = RegisterForm

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = "dashboard:index"  # Cambia esto a la URL a la que deseas redirigir después de iniciar sesión
    # redirect_field_name = 'next'

    def get_success_url(self):
        return "/"  # Cambia esto a la URL a la que deseas redirigir después de iniciar sesión
    