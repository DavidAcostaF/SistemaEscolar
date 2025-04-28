from django.core.management.base import BaseCommand
from apps.users.models import Alumno
from apps.moodle.api_client import call_moodle_api
import requests
from django.core.files.base import ContentFile
import os
from urllib.parse import urlparse


class Command(BaseCommand):
    help = 'Sincroniza alumnos desde Moodle'

    def handle(self, *args, **options):
        print("🔄 Sincronizando alumnos desde Moodle...")

        response = call_moodle_api('core_user_get_users', {'criteria[0][key]': 'email', 'criteria[0][value]': '%'})

        users = response.get('users', [])

        for user_data in users:
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
                    foto_filename_from_url = os.path.basename(urlparse(foto_url).path)
                    foto_guardada_filename = os.path.basename(alumno.foto_archivo.name) if alumno.foto_archivo else None

                    if not foto_guardada_filename or foto_guardada_filename != foto_filename_from_url:
                        response = requests.get(foto_url)
                        if response.status_code == 200:
                            alumno.foto_archivo.save(foto_filename_from_url, ContentFile(response.content), save=True)
                            print(f"🖼️ Foto actualizada para {nombre}")
                    else:
                        print(f"✔️ Foto ya actualizada para {nombre}, no se descargó de nuevo.")

                except Exception as e:
                    print(f"⚠️ Error descargando foto de {nombre}: {e}")

            if created:
                print(f"🧠 Alumno creado: {nombre}")
            else:
                print(f"♻️ Alumno actualizado: {nombre}")

        print("🎯 Sincronización de alumnos completada.")
