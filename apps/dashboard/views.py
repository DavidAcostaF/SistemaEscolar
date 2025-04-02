from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

class MateriasView(TemplateView):
    template_name = 'dashboard/materias.html'

class CalificacionesView(TemplateView):
    template_name = 'dashboard/calificaciones.html'

class TareasPendientesView(TemplateView):
    template_name = 'dashboard/tareas_pendientes.html'

class DescripcionTareaView(TemplateView):
    template_name = 'dashboard/descripcion_tarea.html'

class MensajeriaView(TemplateView):
    template_name = 'dashboard/mensajeria.html'