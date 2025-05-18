# apps/alumnos/controllers.py
from django.core.handlers.wsgi import WSGIRequest
from ninja_extra import api_controller, http_post
from ninja_extra.controllers import ControllerBase
from django.http import JsonResponse
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from apps.comun.auth import APIKeyAuth 
from apps.users.models import Alumno
from apps.moodle.api_client import call_moodle_api
from apps.users.schemas import AlumnoHookIn
import requests, os

@api_controller("/hooks/alumnos", tags=["Alumnos"], auth=APIKeyAuth())
class AlumnosHookController(ControllerBase):

    @http_post("/", url_name="recibir_alumno")
    def recibir_alumno(self, request, data: AlumnoHookIn):
        response = call_moodle_api('core_user_get_users_by_field', {
            'field': 'id',
            'values[0]': data.userid
        })

        if not response:
            print("No se encontró el usuario en Moodle")
            return JsonResponse({"error": "No se encontró el usuario"}, status=404)

        user_data = response[0]
        username = user_data['username']
        nombre = f"{user_data.get('firstname', '')} {user_data.get('lastname', '')}".strip()
        foto_url = user_data.get('profileimageurl', '')

        alumno, created = Alumno.objects.update_or_create(
            alumno_moodle_id=user_data['id'],
            defaults={'nombre': nombre or username, 'username': username}
        )

        if foto_url:
            try:
                foto_filename = os.path.basename(urlparse(foto_url).path)
                guardada = os.path.basename(alumno.foto_archivo.name) if alumno.foto_archivo else None

                if not guardada or guardada != foto_filename:
                    response = requests.get(foto_url)
                    if response.status_code == 200:
                        alumno.foto_archivo.save(foto_filename, ContentFile(response.content), save=True)
            except Exception as e:
                return JsonResponse({"error": f"Error descargando foto: {str(e)}"}, status=500)

        print(f"Alumno {alumno.nombre} {'creado' if created else 'actualizado'}")
        return {"status": "ok", "creado": created}
