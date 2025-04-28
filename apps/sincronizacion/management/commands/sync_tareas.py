from django.core.management.base import BaseCommand
from apps.moodle.api_client import call_moodle_api
from apps.users.models import Alumno
from apps.materias.models import Materia
from apps.tareas.models import Tarea, TareaAlumno
from apps.comun.utils import timestamp_to_datetime
class Command(BaseCommand):
    help = 'Sincroniza las tareas de Moodle con Django'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Sincronizando tareas desde Moodle...')

        alumnos = Alumno.objects.all()
        if not alumnos:
            self.stdout.write('⚠️ No hay alumnos registrados para sincronizar tareas.')
            return

        for alumno in alumnos:
            materias = Materia.objects.filter(alumnos_materia__alumno=alumno).distinct()
            if not materias:
                self.stdout.write(f"⚠️ No se encontraron materias para {alumno.nombre}.")
                continue

            for materia in materias:
                assignments_response = call_moodle_api('mod_assign_get_assignments', {'courseids[0]': materia.materia_moodle_id})
                curso_data = next((c for c in assignments_response.get('courses', []) if c['id'] == materia.materia_moodle_id), None)

                if not curso_data:
                    continue

                for assignment in curso_data.get('assignments', []):
                    tarea, created = Tarea.objects.update_or_create(
                        moodle_id=assignment['id'],
                        defaults={
                            'nombre': assignment['name'],
                            'materia': materia,
                            'descripcion': assignment.get('intro', ''),
                            'fecha_apertura': timestamp_to_datetime(assignment.get('allowsubmissionsfromdate')),
                            'fecha_entrega': timestamp_to_datetime(assignment.get('duedate')),
                        }
                    )


                    # Ahora sincronizamos las entregas y calificaciones
                    grades_response = call_moodle_api('mod_assign_get_grades', {'assignmentids[0]': tarea.moodle_id})

                    for assignment_data in grades_response.get('assignments', []):
                        for grade_data in assignment_data.get('grades', []):
                            if int(grade_data.get('userid')) == alumno.alumno_moodle_id:
                                calificacion = float(grade_data.get('grade')) if grade_data.get('grade') else None
                                entregada = timestamp_to_datetime(grade_data.get('timemodified')) is not None
                                fecha_real = timestamp_to_datetime(grade_data.get('timemodified'))


                                TareaAlumno.objects.update_or_create(
                                    alumno=alumno,
                                    tarea=tarea,
                                    defaults={
                                        'calificacion': calificacion,
                                        'entregada': entregada,
                                        'fecha_entrega_real': fecha_real
                                    }
                                )

                self.stdout.write(f"✅ Tareas sincronizadas para alumno: {alumno.nombre} en materia: {materia.nombre}")

        self.stdout.write('🎯 Sincronización completa de tareas.')
