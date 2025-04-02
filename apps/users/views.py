from django.shortcuts import render
from django.views.generic import View,TemplateView

# Create your views here.


class UserIndexView(TemplateView):
    template_name = 'users/login.html'



class UserRegisterView(TemplateView):
    template_name = 'users/register.html'