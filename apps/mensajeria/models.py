from django.db import models
from apps.users.models import Alumno
from apps.materias.models import Materia
# Create your models here.
class Mensaje(models.Model):
    moodle_id_remitente = models.IntegerField()
    moodle_id_destinatario = models.IntegerField()
    curso_moodle_id = models.IntegerField()
    contenido = models.TextField()
    enviado_por_django = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    recibido = models.DateTimeField(auto_now_add=True)

