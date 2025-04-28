from django.core.management.base import BaseCommand
from apps.users.models import Alumno
from apps.moodle.api_client import call_moodle_api

class Command(BaseCommand):
    help = 'Sincroniza alumnos desde Moodle'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Sincronizando alumnos desde Moodle...')
        
        alumnos = call_moodle_api('core_user_get_users', {
            'criteria[0][key]': 'email',
            'criteria[0][value]': '%'
        })
        for user in alumnos.get('users', []):
            alumno, created = Alumno.objects.update_or_create(
                alumno_moodle_id=user['id'],
                defaults={
                    'nombre': user.get('fullname', ''),
                    'username': user.get('username', ''),
                    'foto_url': user.get('profileimageurl', '')
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Alumno creado: {alumno.nombre}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"♻️ Alumno actualizado: {alumno.nombre}"))
