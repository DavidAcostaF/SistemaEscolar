from django.views import View
from django.shortcuts import render
from django.db.models import Avg, Q
from apps.users.models import Alumno
from apps.tareas.models import TareaAlumno
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.comun.mixins import RedireccionPorRolMixin
from django.contrib.messages.views import SuccessMessageMixin
from collections import defaultdict
from statistics import mean
from apps.materias.models import MateriaAlumno
from django.contrib import messages

class IndexView(RedireccionPorRolMixin,SuccessMessageMixin,View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        alumno = request.user.alumno
        is_staff = request.user.is_staff
        # Calculamos promedio general
        promedio = (
            TareaAlumno.objects
            .filter(alumno=alumno, calificacion__isnull=False)
            .aggregate(promedio=Avg('calificacion'))['promedio']
        )

        if promedio is not None:
            if promedio >= 9:
                rendimiento = 'Alto'
            elif promedio >= 7:
                rendimiento = 'Medio'
            else:
                rendimiento = 'Bajo'
        else:
            rendimiento = "N/A"

        tareas_pendientes = (
            TareaAlumno.objects
            .filter(alumno=alumno, entregada=False)
            .count()
        )
        alertas = obtener_alertas_riesgo_reprobacion(alumno)
        if alertas:
            print(alertas)
            messages.error(request, f"Alertas de riesgo de reprobación: {', '.join(alertas)}")
        context = {
            'alumno': alumno,
            'promedio_general': round(promedio, 2) if promedio else None,
            'rendimiento': rendimiento,
            'tareas_pendientes': tareas_pendientes
        }
        return render(request, self.template_name, context)





def obtener_alertas_riesgo_reprobacion(alumno):
    alertas = []

    materias = MateriaAlumno.objects.filter(alumno=alumno).select_related('materia')

    for mat in materias:
        tareas = mat.materia.tareas.all().prefetch_related('alumnos_tarea')
        calificaciones = defaultdict(list)

        for tarea in tareas:
            tarea_alumno = tarea.alumnos_tarea.filter(alumno=alumno, entregada=True).first()
            if tarea_alumno and tarea_alumno.calificacion is not None:
                parcial = tarea.parcial or "Sin Parcial"
                calificaciones[parcial].append(tarea_alumno.calificacion)

        for parcial, califs in calificaciones.items():
            if califs:
                promedio = round(mean(califs), 2)
                if promedio < 70:
                    alertas.append(f"{mat.materia.nombre} - {parcial} ({promedio})")

    return alertas
