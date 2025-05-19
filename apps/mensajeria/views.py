from django.views.generic import TemplateView, ListView, View
from apps.users.models import User,Alumno
from django.db.models import Exists, OuterRef
from apps.materias.models import MateriaAlumno
from apps.mensajeria.models import Mensaje
from django.shortcuts import get_object_or_404, redirect, render
from apps.materias.models import Materia
from django.urls import reverse_lazy
from apps.mensajeria.forms import MensajeForm

# Create your views here.

class ListaCursosAlumnoView(TemplateView):
    template_name = "mensajeria/lista_cursos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.alumno_id)
        alumno = Alumno.objects.filter(id=self.request.user.alumno_id).first()
        print(alumno)
        if alumno:
            context["cursos"] = MateriaAlumno.objects.filter(
                alumno=alumno,
                rol="student"
            )
        else:
            context["cursos"] = []
        return context


class ListaAlumnosConMensajesView(TemplateView):
    template_name = "mensajeria/lista_maestro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        materias_ids = MateriaAlumno.objects.filter(
            alumno__username=usuario.username,
            rol__in=["editingteacher", "teacher"]
        ).values_list("materia", flat=True)

        alumnos = User.objects.filter(
            Exists(
                Mensaje.objects.filter(
                    materia__in=materias_ids,
                    es_enviado_por_alumno=True,
                    emisor=OuterRef("pk")
                )
            )
        ).distinct()

        context["alumnos"] = alumnos
        return context



class ChatCursoView(View):
    form_class = MensajeForm
    template_name = "mensajeria/mensajeria.html"
    def get(self, request, curso_id):
        materia = get_object_or_404(Materia, id=curso_id)
        mensajes = Mensaje.objects.filter(materia=materia).order_by('fecha')

        es_maestro = MateriaAlumno.objects.filter(
            alumno=request.user.alumno_id,
            materia=materia,
            rol__in=["editingteacher", "teacher"]
        ).exists()

        if es_maestro:
            mensajes = mensajes.filter(es_enviado_por_alumno=True)

        form = None if es_maestro else self.form_class()

        return render(request, "mensajeria/mensajeria.html", {
            "curso": materia,
            "mensajes": mensajes,
            "form": form,
        })

    def post(self, request, curso_id):
        materia = get_object_or_404(Materia, id=curso_id)
        user = request.user

        # Determinar si el usuario es alumno
        try:
            alumno = user.alumno
            es_alumno = MateriaAlumno.objects.filter(
                alumno=alumno,
                materia=materia,
                rol="student"
            ).exists()
        except Alumno.DoesNotExist:
            es_alumno = False

        # Verifica también si es maestro
        es_maestro = user.is_staff
        # Solo permitir si es alumno o maestro
        if not es_alumno and not es_maestro:
            return redirect("mensajeria:enviar_mensaje", curso_id=curso_id)

        form = self.form_class(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.materia = materia
            mensaje.emisor = user
            mensaje.es_enviado_por_alumno = es_alumno
            mensaje.save()

        return redirect("mensajeria:enviar_mensaje", curso_id=curso_id)
