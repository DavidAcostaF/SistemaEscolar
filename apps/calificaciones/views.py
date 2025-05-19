from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,ListView,View
from collections import defaultdict
from django.shortcuts import get_object_or_404
from apps.users.models import Alumno
from apps.tareas.models import TareaAlumno
from apps.comun.mixins import RedireccionPorRolMixin

# Create your views here.
class CalificacionesView(RedireccionPorRolMixin,TemplateView):
    template_name = 'calificaciones/calificaciones.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alumno"] = self.request.user.alumno
        context["etiquetas"] = [
            "Primer año",
            "Segundo año",
            "Tercer año",
            "Cuarto año",
            "Quinto año",
        ]
        return context

class CalificacionesDetallesView(RedireccionPorRolMixin,View):
    model = Alumno
    template_name = "calificaciones/detalle.html"
    context_object_name = "alumno"

    def get(self, request, etiqueta,*args, **kwargs):
        context = {}
        user = self.request.user
        print(user,"user")
        print(user.alumno,"alumno")
        print(etiqueta)
        tareas = TareaAlumno.objects.filter(
            alumno=user.alumno,
            tarea__materia__etiqueta=etiqueta
        ).select_related("tarea__materia")

        materias = defaultdict(list)
        for t in tareas:
            materias[t.tarea.materia.nombre].append({
                "tarea": t.tarea.nombre,
                "calificacion": t.calificacion,
                "entregada": t.entregada,
            })
        context["etiqueta"] = etiqueta
        context["materias"] = dict(materias)
        return render(request, self.template_name, context)
