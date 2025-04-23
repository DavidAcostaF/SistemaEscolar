from django.urls import path
from .views import TareasPendientesView, DescripcionTareaView

app_name = 'tareas'

urlpatterns = [
    path('tareas-pendientes/', TareasPendientesView.as_view(), name='tareas_pendientes'),
    path('descripcion-tarea/', DescripcionTareaView.as_view(), name='descripcion_tarea'),
]