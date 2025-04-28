from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Sincroniza todo desde Moodle (alumnos, cursos, tareas)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando sincronización completa de Moodle...'))

        call_command('sync_alumnos')
        call_command('sync_materias')
        call_command('sync_tareas')

        self.stdout.write(self.style.SUCCESS('✅ Sincronización completa de Moodle.'))
