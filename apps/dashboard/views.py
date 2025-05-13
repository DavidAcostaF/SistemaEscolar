from django.views import View
from django.shortcuts import render
from django.db.models import Avg, Q
from apps.users.models import Alumno
from apps.tareas.models import TareaAlumno

class IndexView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        alumno = request.user.alumno

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
        print(alumno,"alumno")
        context = {
            'alumno': alumno,
            'promedio_general': round(promedio, 2) if promedio else None,
            'rendimiento': rendimiento,
            'tareas_pendientes': tareas_pendientes
        }
        return render(request, self.template_name, context)
