from django.db import models
from apps.users.models import Alumno, User
from apps.materias.models import Materia
# Create your models here.

class Mensaje(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    es_enviado_por_alumno = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.emisor.username} - {self.materia.nombre[:30]}"


