from django.db import models
from apps.users.models import User

class Materia(models.Model):
    curso_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
