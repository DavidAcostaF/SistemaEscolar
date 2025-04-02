from django.urls import path
from .views import IndexView, MateriasView, CalificacionesView, TareasPendientesView, DescripcionTareaView,MensajeriaView

app_name = 'dashboard'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('materias/', MateriasView.as_view(), name='materias'),
    path('calificaciones/', CalificacionesView.as_view(), name='calificaciones'),
    path('tareas-pendientes/', TareasPendientesView.as_view(), name='tareas_pendientes'),
    path('descripcion-tarea/', DescripcionTareaView.as_view(), name='descripcion_tarea'),
    path('mensajeria/', MensajeriaView.as_view(), name='mensajeria'),
]