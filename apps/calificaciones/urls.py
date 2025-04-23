from django.urls import path
from .views import  CalificacionesView
app_name = 'calificaciones'

urlpatterns = [
    path('calificaciones/', CalificacionesView.as_view(), name='calificaciones'),
]