import logging
from ninja_extra import api_controller, http_post,route
from ninja_extra.controllers import ControllerBase
from django.http import JsonResponse
from .schemas import TareaCrearHookIn, TareaCalificarHookIn
from apps.users.models import Alumno
from apps.materias.models import Materia, MateriaAlumno
from apps.tareas.models import Tarea, TareaAlumno
from apps.moodle.api_client import call_moodle_api
from apps.comun.utils import timestamp_to_datetime
import time

@api_controller("/hooks/tarea", tags=["Tareas"])
class TareasHookController(ControllerBase):

    @route.post("/crear/", url_name="crear_tarea")
    def crear_tarea(self, request, tarea: TareaCrearHookIn):
        materia = Materia.objects.filter(moodle_id=tarea.courseid).first()
        if not materia:
            return JsonResponse({"error": "La materia con ese Moodle ID no existe"}, status=404)

        intento = 0
        tarea_moodle = None

        while True:
            intento += 1
            print(f"🔄 Intento #{intento} de obtener tarea con cmid {tarea.cmid}")
            tareas_response = call_moodle_api("mod_assign_get_assignments", {
                "courseids[0]": tarea.courseid
            })

            for curso in tareas_response.get("courses", []):
                for asignacion in curso.get("assignments", []):
                    if asignacion["cmid"] == tarea.cmid:
                        tarea_moodle = asignacion
                        break
                if tarea_moodle:
                    break

            if tarea_moodle:
                break

            print("⏳ Tarea no encontrada aún, esperando 3 segundos...")
            time.sleep(3)
        # Obtener sección (parcial)
        parcial = "Sin parcial"
        try:
            secciones_response = call_moodle_api("core_course_get_contents", {
                "courseid": tarea.courseid
            })
            for seccion in secciones_response:
                for modulo in seccion.get("modules", []):
                    if modulo["id"] == tarea.cmid:
                        parcial = seccion.get("name", "Sin parcial")
                        break
                if parcial != "Sin parcial":
                    break
        except Exception as e:
            print(f"⚠️ Error al obtener la sección: {e}")
        print(tarea_moodle)
        tarea, _ = Tarea.objects.update_or_create(
            moodle_id=tarea_moodle["cmid"],  # ← Este es el cmid, identificador único de la tarea
            defaults={
                "moodle_assign_id": tarea_moodle["id"],  # ← Este es el assign.id (para usar en get_grades)
                "nombre": tarea_moodle.get("name", "Sin nombre"),
                "descripcion": tarea_moodle.get("intro", ""),
                "fecha_apertura": timestamp_to_datetime(tarea_moodle.get("allowsubmissionsfromdate")),
                "fecha_entrega": timestamp_to_datetime(tarea_moodle.get("duedate")),
                "materia": materia,
                "parcial": parcial
            }
        )

        alumnos = Alumno.objects.filter(materias_alumno__materia=materia).distinct()
        creados = 0
        for alumno in alumnos:
            _, creado = TareaAlumno.objects.get_or_create(
                tarea=tarea,
                alumno=alumno,
                defaults={"entregada": False}
            )
            if creado:
                creados += 1

        return {"status": "ok", "mensaje": f"Tarea creada y asignada a {creados} alumno(s)"}

    @route.post("/calificada/", url_name="calificar_tarea")
    def calificar_tarea(self, request, data: TareaCalificarHookIn):
        print(data)
        print(f"🔄 Calificando tarea con ID {data.tareaid} para el usuario {data.userid}")

        # Buscar tarea por cmid
        tarea = Tarea.objects.filter(moodle_id=data.cmid).first()
        if not tarea:
            print(f"⚠️ Tarea con cmid {data.cmid} no encontrada")
            return JsonResponse({"error": "Tarea no encontrada"}, status=404)

        try:
            alumno = Alumno.objects.get(alumno_moodle_id=data.userid)
        except Alumno.DoesNotExist:
            print(f"⚠️ Alumno con ID {data.userid} no encontrado")
            return JsonResponse({"error": "Alumno no encontrado"}, status=404)

        # Usar el assign.id guardado en moodle_assign_id para consultar la nota
        assignid = tarea.moodle_assign_id
        if not assignid:
            print("⚠️ La tarea no tiene assignid asociado (moodle_assign_id está vacío)")
            return JsonResponse({"error": "Tarea sin assignid"}, status=400)

        grades_response = call_moodle_api("mod_assign_get_grades", {
            "assignmentids[0]": assignid
        })
        print("📦 Response de mod_assign_get_grades:", grades_response)

        calificacion = None
        entregada = False

        for assignment in grades_response.get("assignments", []):
            for grade in assignment.get("grades", []):
                if int(grade.get("userid")) == alumno.alumno_moodle_id:
                    if grade.get("grade") is not None:
                        calificacion = float(grade.get("grade"))
                        entregada = True

        obj, creado = TareaAlumno.objects.update_or_create(
            tarea=tarea,
            alumno=alumno,
            defaults={"calificacion": calificacion, "entregada": entregada}
        )
        print("🎯 Registro", "creado" if creado else "actualizado", obj.calificacion)

        return {"status": "ok", "mensaje": "Calificación registrada"}


