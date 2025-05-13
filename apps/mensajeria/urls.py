from django.urls import path
from .views import ChatCursoView,ListaCursosAlumnoView

app_name = 'mensajeria'

urlpatterns = [
    path('mensajeria/', ListaCursosAlumnoView.as_view(), name='lista_cursos'),
    path('enviar-mensaje/<int:curso_id>/', ChatCursoView.as_view(), name='enviar_mensaje'),
]