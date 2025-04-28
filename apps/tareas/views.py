from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from apps.moodle import api_client
from apps.comun.utils import format_fecha
import datetime
# Create your views here.

class TareasPendientesView(LoginRequiredMixin, View):
    template_name = 'tareas/tareas_pendientes.html'

    def get(self, request):
        alumno_id = request.user.alumno_moodle_id
        materias = api_client.get_tareas_pendientes_por_curso(alumno_id)
        return render(request, self.template_name, {'materias': materias})


class DetalleTareaView(LoginRequiredMixin, View):
    template_name = 'tareas/detalle_tarea.html'

    def get(self, request, curso_id, tarea_id):
        assignments_response = api_client.call_moodle_api('mod_assign_get_assignments', {'courseids[0]': curso_id})
        tarea = None

        for course in assignments_response.get('courses', []):
            if course['id'] == curso_id:
                for assign in course.get('assignments', []):
                    if assign['id'] == tarea_id:
                        tarea = assign
                        break

        if not tarea:
            return render(request, '404.html')


        allowsubmissionsfromdate_str, allowsubmissionsfromdate_dt = format_fecha(tarea.get('allowsubmissionsfromdate', None))
        duedate_str, duedate_dt = format_fecha(tarea.get('duedate', None))
        cutoffdate_str, cutoffdate_dt = format_fecha(tarea.get('cutoffdate', None))

        estado_entrega = "No disponible"
        if duedate_dt:
            now = datetime.datetime.now()
            if now > duedate_dt:
                estado_entrega = "Entrega vencida"
            else:
                estado_entrega = "A tiempo"

        contexto = {
            'nombre': tarea.get('name', 'Sin nombre'),
            'intro': tarea.get('intro', 'Sin instrucciones disponibles'),
            'allowsubmissionsfromdate': allowsubmissionsfromdate_str,
            'duedate': duedate_str,
            'cutoffdate': cutoffdate_str,
            'estado_entrega': estado_entrega,
        }
        return render(request, self.template_name, contexto)