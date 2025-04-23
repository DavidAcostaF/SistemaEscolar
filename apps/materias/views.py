from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class MateriasView(TemplateView):
    template_name = 'materias/materias.html'