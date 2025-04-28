from django.core.management.base import BaseCommand
from apps.moodle.api_client import call_moodle_api
from apps.materias.models import Materia, MateriaAlumno
from apps.users.models import Alumno

class Command(BaseCommand):
    help = 'Sincroniza las materias (cursos) de Moodle con Django'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Sincronizando materias desde Moodle...')

        alumnos = Alumno.objects.all()
        if not alumnos:
            self.stdout.write('⚠️ No hay alumnos para sincronizar materias.')
            return

        for alumno in alumnos:
            # Obtener cursos (materias) inscritos por alumno
            cursos = call_moodle_api('core_enrol_get_users_courses', {'userid': alumno.alumno_moodle_id})
            if not cursos:
                self.stdout.write(f"⚠️ No se encontraron materias para {alumno.nombre}.")
                continue

            for curso in cursos:
                materia, created = Materia.objects.update_or_create(
                    moodle_id=curso['id'],
                    defaults={'nombre': curso['fullname']}
                )

                # Relacionar alumno con materia
                MateriaAlumno.objects.get_or_create(
                    alumno=alumno,
                    materia=materia
                )

                if created:
                    self.stdout.write(f"📚 Materia creada: {materia.nombre}")
                else:
                    self.stdout.write(f"♻️ Materia actualizada: {materia.nombre}")

            self.stdout.write(f"✅ Materias sincronizadas para alumno: {alumno.nombre}")

        self.stdout.write('🎯 Sincronización completa de materias.')
