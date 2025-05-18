from django.urls import path
from .views import  CalificacionesView,CalificacionesDetallesView
app_name = 'calificaciones'

urlpatterns = [
    path('calificaciones/', CalificacionesView.as_view(), name='calificaciones'),
    path('calificaciones/<str:etiqueta>/', CalificacionesDetallesView.as_view(), name='detalle'),
]