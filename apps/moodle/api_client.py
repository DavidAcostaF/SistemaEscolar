import requests
from django.conf import settings

def get_cursos_por_usuario(user_id):
    params = {
        'wstoken': settings.MOODLE_TOKEN,
        'wsfunction': 'core_enrol_get_users_courses',
        'moodlewsrestformat': 'json',
        'userid': user_id
    }
    response = requests.get(settings.MOODLE_API_URL, params=params)
    response.raise_for_status()
    return response.json()
