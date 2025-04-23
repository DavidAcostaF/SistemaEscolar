from django.shortcuts import render
from django.views.generic import View,TemplateView,CreateView
from .models import User
from .forms import RegisterForm
# Create your views here.


class UserIndexView(CreateView):
    template_name = 'users/login.html'
    model = User


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = RegisterForm