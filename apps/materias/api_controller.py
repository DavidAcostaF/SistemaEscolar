# api/hooks/controllers/materias_controller.py
from ninja_extra import api_controller, http_post
from ninja_extra.controllers import ControllerBase
from django.http import JsonResponse
from apps.moodle.api_client import call_moodle_api
from apps.materias.models import Materia, MateriaAlumno
from apps.users.models import Alumno
from apps.materias.schemas import MateriaHookIn
from apps.comun.auth import APIKeyAuth
import time
from apps.comun.utils import timestamp_to_datetime
from django.contrib.auth.hashers import make_password
from apps.users.models import User

@api_controller("/hooks/materias/", tags=["Materias"], auth=APIKeyAuth())
class MateriasHookController(ControllerBase):

    @http_post("/", url_name="recibir_materias")
    def recibir_materias(self, request, data: MateriaHookIn):
        try:
            alumno = Alumno.objects.get(alumno_moodle_id=data.userid)
        except Alumno.DoesNotExist:
            return JsonResponse({"error": "Alumno no encontrado en Django"}, status=404)

        cursos = call_moodle_api('core_enrol_get_users_courses', {'userid': data.userid})
        if not cursos:
            return {"status": "ok", "materias": [], "mensaje": "Sin cursos encontrados"}

        materias_creadas = []

        for curso in cursos:
            print(f"Curso: {curso}")

            categorias = call_moodle_api('core_course_get_categories', {
                'criteria[0][key]': 'id',
                'criteria[0][value]': curso['category']
            })
            etiqueta = categorias[0]['name'] if categorias else 'Sin categoría'

            materia, created = Materia.objects.update_or_create(
                moodle_id=curso['id'],
                defaults={
                    'nombre': curso['fullname'],
                    'etiqueta': etiqueta
                }
            )

            rol = None
            email = None
            intentos = 0
            max_intentos = 10

            while intentos < max_intentos:
                intentos += 1
                try:
                    usuarios = call_moodle_api('core_enrol_get_enrolled_users', {
                        'courseid': curso['id']
                    })

                    for u in usuarios:
                        if u['id'] == data.userid:
                            roles = u.get('roles', [])
                            if roles:
                                rol = roles[0]['shortname']
                                email = u.get('email', None)
                                print(f"✅ Rol encontrado en intento #{intentos}: {rol}")
                                break
                            else:
                                print(f"⏳ Usuario encontrado sin roles. Intento #{intentos}")
                    if rol:
                        break
                except Exception as e:
                    print(f"⚠️ Error al obtener roles: {e}")

                time.sleep(2)
            print(f"Rol final: {rol}")

            if rol in ["editingteacher"]:
                try:
                    user, creado = User.objects.get_or_create(
                        username=alumno.username,
                        defaults={
                            "email": email,
                            "password": make_password("123"),
                            "first_name": alumno.nombre.split(" ")[0],
                            "last_name": " ".join(alumno.nombre.split(" ")[1:]),
                            "is_staff": True,
                        }
                    )
                    if creado:
                        print(f"✅ Usuario Django creado para maestro: {user.username}")
                    else:
                        print(f"ℹ️ Usuario Django ya existía: {user.username}")
                except Exception as e:
                    print(f"❌ Error creando usuario Django: {e}")


            MateriaAlumno.objects.update_or_create(
                alumno=alumno,
                materia=materia,
                defaults={"rol": rol or "student"}
            )

            materias_creadas.append({
                "nombre": materia.nombre,
                "etiqueta": materia.etiqueta,
                "creada": created
            })

        return {
            "status": "ok",
            "materias": materias_creadas
        }












































































































































































































































































































































































































































































































































































































































































































































































































































































































































































