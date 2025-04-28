from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from .forms import SeleccionarAlumnoForm
from apps.moodle import api_client
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class MateriasView(View):
    template_name = 'materias/materias.html'

    def get(self, request):
        alumno_id = request.user.alumno_moodle_id
        materias = api_client.get_materias_con_promedios_por_parcial(alumno_id)
        return render(request, self.template_name, {'materias': materias})

