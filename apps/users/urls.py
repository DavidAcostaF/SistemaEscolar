from django.urls import path
from .views import UserIndexView, UserRegisterView

app_name = 'users'

urlpatterns = [
    path('login/', UserIndexView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
]