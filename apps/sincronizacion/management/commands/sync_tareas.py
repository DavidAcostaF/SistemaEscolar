from django.core.management.base import BaseCommand
from apps.moodle.api_client import call_moodle_api
from apps.users.models import Alumno
from apps.materias.models import Materia
from apps.tareas.models import Tarea, TareaAlumno
from apps.comun.utils import timestamp_to_datetime
from apps.materias.models import MateriaAlumno
class Command(BaseCommand):
    help = 'Sincroniza tareas y entregas desde Moodle'

    def handle(self, *args, **options):
        print("🔄 Sincronizando tareas desde Moodle...")

        alumnos = Alumno.objects.all()
        for alumno in alumnos:
            materias_alumno = MateriaAlumno.objects.filter(alumno=alumno).select_related('materia')

            if not materias_alumno.exists():
                print(f"⚠️ No se encontraron materias para {alumno.nombre}.")
                continue

            for materia_alumno in materias_alumno:
                materia = materia_alumno.materia

                # 1️⃣ Obtener las secciones del curso (parciales)
                secciones_response = call_moodle_api('core_course_get_contents', {
                    'courseid': materia.moodle_id
                })

                # 2️⃣ Mapear tareas por sección
                for seccion in secciones_response:
                    nombre_seccion = seccion.get('name', 'Sin sección').strip() or 'Sin sección'

                    for modulo in seccion.get('modules', []):
                        if modulo.get('modname') == 'assign':
                            tarea_id = modulo['instance']

                            # 3️⃣ Consultar detalles de la tarea (debería hacerse mejor pero con la info del módulo es suficiente)
                            tareas_response = call_moodle_api('mod_assign_get_assignments', {
                                'courseids[0]': materia.moodle_id
                            })

                            cursos_data = tareas_response.get('courses', [])
                            if not cursos_data:
                                continue

                            tarea_moodle = next(
                                (t for t in cursos_data[0]['assignments'] if t['id'] == tarea_id),
                                None
                            )
                            if not tarea_moodle:
                                continue

                            tarea, created = Tarea.objects.update_or_create(
                                moodle_id=tarea_moodle['id'],
                                defaults={
                                    'nombre': tarea_moodle.get('name', 'Sin nombre'),
                                    'descripcion': tarea_moodle.get('intro', ''),
                                    'fecha_apertura': timestamp_to_datetime(tarea_moodle.get('allowsubmissionsfromdate')),
                                    'fecha_entrega': timestamp_to_datetime(tarea_moodle.get('duedate')),
                                    'materia': materia,
                                    'parcial': nombre_seccion
                                }
                            )

                            # 4️⃣ Obtener calificaciones de la tarea
                            grades_response = call_moodle_api('mod_assign_get_grades', {
                                'assignmentids[0]': tarea.moodle_id
                            })

                            for assignment in grades_response.get('assignments', []):
                                for grade in assignment.get('grades', []):
                                    if int(grade.get('userid')) == alumno.alumno_moodle_id:
                                        TareaAlumno.objects.update_or_create(
                                            tarea=tarea,
                                            alumno=alumno,
                                            defaults={
                                                'calificacion': float(grade.get('grade')) if grade.get('grade') is not None else None,
                                                'entregada': grade.get('grade') is not None,
                                            }
                                        )

                print(f"♻️ Tareas sincronizadas para materia: {materia.nombre} ({alumno.nombre})")
        
        print("🎯 Sincronización completa de tareas.")
