from django.urls import path
from .views import  MateriasView

app_name = 'materias'

urlpatterns = [
    path('materias/', MateriasView.as_view(), name='materias'),
]