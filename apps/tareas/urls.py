from django.urls import path
from .views import TareasPendientesView, DetalleTareaView

app_name = 'tareas'

urlpatterns = [
    path('tareas-pendientes/', TareasPendientesView.as_view(), name='tareas_pendientes'),
    path('detalle-tarea/<int:curso_id>/<int:tarea_id>/', DetalleTareaView.as_view(), name='detalle_tarea'),
]