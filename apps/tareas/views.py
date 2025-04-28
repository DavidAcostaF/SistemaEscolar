from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.moodle import api_client
import datetime
from apps.materias.models import MateriaAlumno
from apps.tareas.models import Tarea, TareaAlumno
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


# Create your views here.

class TareasPendientesView(LoginRequiredMixin, View):
    template_name = 'tareas/tareas_pendientes.html'

    def get(self, request):
        alumno = request.user.alumno

        materias_data = []

        materias_alumno = MateriaAlumno.objects.filter(
            alumno=alumno
        ).select_related('materia')

        for materia_alumno in materias_alumno:
            materia = materia_alumno.materia

            tareas_pendientes = TareaAlumno.objects.filter(
                alumno=alumno,
                tarea__materia=materia,
                entregada=False
            ).select_related('tarea')

            tareas_info = []
            for tarea_alumno in tareas_pendientes:
                tarea = tarea_alumno.tarea
                tareas_info.append({
                    'id': tarea.id,
                    'nombre': tarea.nombre,
                    'intro': tarea.descripcion or '',
                    'duedate': tarea.fecha_entrega.strftime('%d/%m/%Y') if tarea.fecha_entrega else 'Sin fecha'
                })

            if tareas_info:
                materias_data.append({
                    'id': materia.id,
                    'nombre': materia.nombre,
                    'tareas': tareas_info
                })

        return render(request, self.template_name, {'materias': materias_data})


class DetalleTareaView(LoginRequiredMixin, View):
    template_name = 'tareas/detalle_tarea.html'

    def get(self, request, curso_id, tarea_id):
        tarea = get_object_or_404(Tarea, id=tarea_id, materia__id=curso_id)

        allowsubmissionsfromdate_str = tarea.fecha_apertura.strftime('%d/%m/%Y') if tarea.fecha_apertura else "No disponible"
        duedate_str = tarea.fecha_entrega.strftime('%d/%m/%Y') if tarea.fecha_entrega else "No disponible"
        cutoffdate_str = "No disponible"  

        estado_entrega = "No disponible"
        if tarea.fecha_entrega:
            now = timezone.now()
            if now > tarea.fecha_entrega:
                estado_entrega = "Entrega vencida"
            else:
                estado_entrega = "A tiempo"

        contexto = {
            'nombre': tarea.nombre,
            'intro': tarea.descripcion or "Sin instrucciones disponibles",
            'allowsubmissionsfromdate': allowsubmissionsfromdate_str,
            'duedate': duedate_str,
            'cutoffdate': cutoffdate_str,
            'estado_entrega': estado_entrega,
        }
        return render(request, self.template_name, contexto)