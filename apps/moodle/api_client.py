import requests
from django.conf import settings
from collections import defaultdict
from statistics import mean
from django.conf import settings

# TODO: A lo mejor hacer una clase por cada modulo con sus respectivas api's calls

def call_moodle_api(wsfunction, params=None):
    """
    Hace una llamada genérica a la API REST de Moodle.

    :param wsfunction: Nombre de la función a ejecutar (por ejemplo, 'core_enrol_get_users_courses')
    :param params: Diccionario con parámetros adicionales
    :return: Resultado JSON de la respuesta
    """
    if params is None:
        params = {}

    base_params = {
        'wstoken': settings.MOODLE_TOKEN,
        'moodlewsrestformat': 'json',
        'wsfunction': wsfunction,
    }

    response = requests.get(settings.MOODLE_API_URL, params={**base_params, **params})
    response.raise_for_status()
    return response.json()

# MATERIAS
def get_materias_con_promedios_por_parcial(user_id):
    cursos = call_moodle_api('core_enrol_get_users_courses', {'userid': user_id})
    materias = []

    for curso in cursos:
        curso_id = curso['id']
        curso_nombre = curso['fullname']
        calificaciones_por_seccion = defaultdict(list)
        nombres_secciones = []

        secciones_response = call_moodle_api('core_course_get_contents', {'courseid': curso_id})

        for seccion in secciones_response:
            nombre_seccion = seccion.get('name', 'Sin sección').strip().lower()
            if nombre_seccion:
                nombres_secciones.append(nombre_seccion)

            for modulo in seccion.get('modules', []):
                if modulo.get('modname') == 'assign':
                    tarea_id = modulo['instance']

                    grades_response = call_moodle_api('mod_assign_get_grades', {'assignmentids[0]': tarea_id})

                    for assignment in grades_response.get('assignments', []):
                        for grade in assignment.get('grades', []):
                            if int(grade.get('userid')) == user_id:
                                try:
                                    cal = float(grade.get('grade'))
                                    calificaciones_por_seccion[nombre_seccion].append(cal)
                                except (ValueError, TypeError):
                                    pass

        parciales = []
        for nombre_seccion in nombres_secciones:
            calificaciones = calificaciones_por_seccion.get(nombre_seccion, [])
            promedio = round(mean(calificaciones), 2) if calificaciones else "—"
            parciales.append({
                'nombre': nombre_seccion.title(),
                'promedio': promedio
            })

        materias.append({
            'id': curso_id,
            'nombre': curso_nombre,
            'parciales': parciales
        })

    return materias

# TAREAS
def get_tareas_pendientes_por_curso(user_id):
    cursos = call_moodle_api('core_enrol_get_users_courses', {'userid': user_id})
    tareas_pendientes = []

    for curso in cursos:
        curso_id = curso['id']
        curso_nombre = curso['fullname']
        tareas_no_calificadas = []

        secciones_response = call_moodle_api('core_course_get_contents', {'courseid': curso_id})

        for seccion in secciones_response:
            for modulo in seccion.get('modules', []):
                if modulo.get('modname') == 'assign':
                    tarea_id = modulo['instance']
                    tarea_nombre = modulo.get('name', 'Sin nombre')
                    intro = modulo.get('description', '')
                    duedate = modulo.get('availability', '')

                    grades_response = call_moodle_api('mod_assign_get_grades', {'assignmentids[0]': tarea_id})

                    encontrado = False
                    for assignment in grades_response.get('assignments', []):
                        for grade in assignment.get('grades', []):
                            if int(grade.get('userid')) == user_id:
                                if grade.get('grade') is not None:
                                    encontrado = True
                                    break

                    if not encontrado:
                        tareas_no_calificadas.append({
                            'id': tarea_id,
                            'nombre': tarea_nombre,
                            'intro': intro,
                            'duedate': duedate
                        })

        tareas_pendientes.append({
            'id': curso_id,
            'nombre': curso_nombre,
            'tareas': tareas_no_calificadas
        })

    return tareas_pendientes
