from django.urls import path
from .views import ListaCursosAlumnoView, ListaAlumnosConMensajesView, ChatCursoView

app_name = 'mensajeria'

urlpatterns = [
    path("alumno/", ListaCursosAlumnoView.as_view(), name="lista_cursos"),
    path("maestro/", ListaAlumnosConMensajesView.as_view(), name="lista_alumnos"),
    path("curso/<int:curso_id>/", ChatCursoView.as_view(), name="enviar_mensaje")
    # path('enviar-mensaje/<int:curso_id>/', ChatCursoView.as_view(), name='enviar_mensaje'),
]