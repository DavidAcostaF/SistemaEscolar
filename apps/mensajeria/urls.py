from django.urls import path
from .views import MensajeriaView

app_name = 'mensajeria'

urlpatterns = [
    path('mensajeria/', MensajeriaView.as_view(), name='mensajeria'),
]