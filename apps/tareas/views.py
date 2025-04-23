from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class TareasPendientesView(TemplateView):
    template_name = 'tareas/tareas_pendientes.html'



class DescripcionTareaView(TemplateView):
    template_name = 'tareas/descripcion_tarea.html'
