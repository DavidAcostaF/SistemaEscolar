from datetime import datetime

def format_fecha(valor):
    if valor and valor != 0:
        fecha = datetime.fromtimestamp(valor)
        return fecha.strftime("%d %b %Y %H:%M"), fecha
    return None, None



def timestamp_to_datetime(timestamp):
    if timestamp and isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp)
    return None
