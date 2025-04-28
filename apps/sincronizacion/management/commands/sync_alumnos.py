from django.core.management.base import BaseCommand
from apps.users.models import Alumno
from apps.moodle.api_client import call_moodle_api
import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Sincroniza alumnos desde Moodle'

    def handle(self, *args, **options):
        print("🔄 Sincronizando alumnos desde Moodle...")
        response = call_moodle_api('core_user_get_users', {
            'criteria[0][key]': 'email',
            'criteria[0][value]': '%'
        })
        users = response.get('users', [])
        print(f"👥 Total de usuarios encontrados: {len(users)}")
        for user_data in users:
            print(f"🔍 Procesando usuario: {user_data}")
            username = user_data['username']
            nombre = f"{user_data.get('firstname', '')} {user_data.get('lastname', '')}".strip()
            foto_url = user_data.get('profileimageurl', '')
            alumno, created = Alumno.objects.update_or_create(
                alumno_moodle_id=user_data['id'],
                defaults={
                    'nombre': nombre or username,
                    'username': username
                }
            )

            if foto_url:
                try:
                    response = requests.get(foto_url)
                    if response.status_code == 200:
                        file_name = f"{username}.jpg"
                        alumno.foto_archivo.save(file_name, ContentFile(response.content), save=True)
                        print(f"🖼️ Foto guardada para {nombre}")
                except Exception as e:
                    print(f"⚠️ Error descargando foto de {nombre}: {e}")

            if created:
                print(f"🧠 Alumno creado: {nombre}")
            else:
                print(f"♻️ Alumno actualizado: {nombre}")

        print("🎯 Sincronización de alumnos completada.")
