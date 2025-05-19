from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from .forms import SeleccionarAlumnoForm
from apps.moodle import api_client
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.materias.models import MateriaAlumno
from statistics import mean
from collections import defaultdict
from apps.tareas.models import TareaAlumno
from apps.tareas.models import Tarea
from apps.comun.mixins import RedireccionPorRolMixin
# Create your views here.

class MateriasView(RedireccionPorRolMixin,ListView):
    template_name = 'materias/materias.html'
    context_object_name = 'materias'

    def get_queryset(self):
        return MateriaAlumno.objects.filter(
            alumno=self.request.user.alumno
        ).select_related('materia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        materias_data = []
        for materia_alumno in context['materias']:
            materia = materia_alumno.materia

            tareas_alumno = TareaAlumno.objects.filter(
                tarea__materia=materia,
                alumno=self.request.user.alumno,
                entregada=True
            ).select_related('tarea')

            calificaciones_por_parcial = defaultdict(list)
            for tarea_alumno in tareas_alumno:
                parcial = tarea_alumno.tarea.parcial if tarea_alumno.tarea.parcial else 'Sin Parcial'
                if tarea_alumno.calificacion is not None:
                    calificaciones_por_parcial[parcial].append(tarea_alumno.calificacion)

            parciales_definidos = ['Parcial 1', 'Parcial 2', 'Parcial 3']

            parciales = []
            for nombre_parcial in parciales_definidos:
                calificaciones = calificaciones_por_parcial.get(nombre_parcial, [])
                promedio = round(mean(calificaciones), 2) if calificaciones else "—"
                parciales.append({
                    'nombre': nombre_parcial,
                    'promedio': promedio
                })

            materias_data.append({
                'nombre': materia.nombre,
                'parciales': parciales
            })

        context['materias'] = materias_data
        return context
