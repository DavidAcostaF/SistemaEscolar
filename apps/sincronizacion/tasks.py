from django_q.models import Schedule
from django.utils import timezone

def programar_sync_moodle():
    nombre_tarea = "Sync Moodle cada hora"

    defaults = {
        'func': 'django.core.management.call_command',
        'args': "'sync_moodle'",  
        'schedule_type': Schedule.MINUTES,
        'minutes': 1,  
        'repeats': -1,
        'next_run': timezone.now(),
    }

    schedule, created = Schedule.objects.update_or_create(
        name=nombre_tarea,
        defaults=defaults
    )

    if created:
        print(f"✅ Tarea '{nombre_tarea}' creada correctamente.")
    else:
        print(f"♻️ Tarea '{nombre_tarea}' actualizada correctamente.")
