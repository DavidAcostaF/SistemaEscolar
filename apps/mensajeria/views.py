from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from apps.materias.models import MateriaAlumno
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from apps.mensajeria.models import Mensaje
from apps.mensajeria.forms import MensajeForm
from apps.materias.models import Materia
from apps.users.models import Alumno
from apps.moodle.api_client import call_moodle_api, enviar_mensaje_a_maestro
from datetime import datetime

# Create your views here.

class ListaCursosAlumnoView(ListView):
    template_name = "mensajeria/lista_cursos.html"
    context_object_name = "cursos"

    def get_queryset(self):
        return MateriaAlumno.objects.filter(alumno=self.request.user.alumno).select_related("materia")

class ChatCursoView(View):
    def get(self, request, curso_id):
        alumno = request.user.alumno
        curso = get_object_or_404(Materia, id=curso_id)

        mensajes = Mensaje.objects.filter(
            curso_moodle_id=curso.moodle_id
        ).filter(
            moodle_id_remitente=alumno.alumno_moodle_id
        ) | Mensaje.objects.filter(
            curso_moodle_id=curso.moodle_id,
            moodle_id_destinatario=alumno.alumno_moodle_id
        )

        mensajes = mensajes.order_by("timestamp")
        form = MensajeForm()

        return render(request, "mensajeria/mensajeria.html", {
            "alumno": alumno,
            "curso": curso,
            "mensajes": mensajes,
            "form": form,
        })

    def post(self, request, curso_id):
        alumno = request.user.alumno
        curso = get_object_or_404(Materia, id=curso_id)
        form = MensajeForm(request.POST)

        if form.is_valid():
            contenido = form.cleaned_data["contenido"]

            # Buscar maestro en Moodle
            respuesta = call_moodle_api("core_enrol_get_enrolled_users", {
                "courseid": curso.moodle_id
            })

            maestro = next((u for u in respuesta if any(
                r['shortname'] in ["editingteacher", "teacher"] for r in u["roles"]
            )), None)

            if maestro:
                enviar_mensaje_como_intermediario(
                    id_destinatario=maestro["id"],
                    nombre_alumno=alumno.nombre,
                    contenido=contenido
                )

                Mensaje.objects.create(
                    moodle_id_remitente=alumno.alumno_moodle_id,
                    moodle_id_destinatario=maestro["id"],
                    curso_moodle_id=curso.moodle_id,
                    contenido=contenido,
                    timestamp=datetime.now(),
                    enviado_por_django=True
                )

        return redirect("mensajeria:enviar_mensaje", curso_id=curso_id)
    
def enviar_mensaje_como_intermediario(id_destinatario, nombre_alumno, contenido):
    mensaje_decorado = f"[Alumno: {nombre_alumno}] {contenido}"

    data = {
        "messages[0][touserid]": id_destinatario,
        "messages[0][text]": mensaje_decorado,
        "messages[0][textformat]": 1,
    }

    respuesta = call_moodle_api("core_message_send_instant_messages", data)

    if isinstance(respuesta, list) and "id" in respuesta[0]:
        print("✅ Mensaje enviado correctamente desde el intermediario.")
        return True
    else:
        print("❌ Error al enviar el mensaje:", respuesta)
        return False