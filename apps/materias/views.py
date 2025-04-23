from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from .forms import SeleccionarAlumnoForm
from apps.moodle.api_client import get_cursos_por_usuario

# Create your views here.
class MateriasView(TemplateView):
    template_name = 'materias/materias.html'


class MateriasView(View):
    template_name = 'materias/materias.html'

    def get(self, request):
        form = SeleccionarAlumnoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SeleccionarAlumnoForm(request.POST)
        materias = []
        if form.is_valid():
            alumno_id = form.cleaned_data['alumno_id']
            datos = get_cursos_por_usuario(alumno_id)

            for curso in datos:
                materias.append({
                    'id': curso['id'],
                    'fullname': curso['fullname'],
                    'shortname': curso['shortname'],
                    'summary': curso.get('summary', '')
                })

        return render(request, self.template_name, {
            'form': form,
            'materias': materias
        })


class DetalleMateriaView(View):
    template_name = 'materias/detalle_materia.html'

    def get(self, request, curso_id):
        # Aquí podrías en el futuro mostrar más detalles usando otra API
        return render(request, self.template_name, {'curso_id': curso_id})