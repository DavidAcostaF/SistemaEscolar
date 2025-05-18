from django.shortcuts import render, redirect
from django.views.generic import View,TemplateView,CreateView
from .models import User
from .forms import RegisterForm,LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy



# Create your views here.


class UserIndexView(CreateView):
    template_name = 'users/login.html'
    model = User

class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = "dashboard:index"  

    def get_success_url(self):
        return "/" 
    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login') 