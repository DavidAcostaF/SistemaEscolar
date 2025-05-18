from datetime import datetime
from django.conf import settings
from django.utils import timezone

def format_fecha(valor):
    if valor and valor != 0:
        fecha = datetime.fromtimestamp(valor)
        return fecha.strftime("%d %b %Y %H:%M"), fecha
    return None, None


def timestamp_to_datetime(timestamp):
    if not timestamp:
        return None
    dt = datetime.fromtimestamp(timestamp)
    if settings.USE_TZ:
        return timezone.make_aware(dt)
    return dt

