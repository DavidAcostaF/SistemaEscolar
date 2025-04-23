from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.



class MensajeriaView(TemplateView):
    template_name = 'mensajeria/mensajeria.html'