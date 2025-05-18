from django.contrib.auth.models import AbstractUser
from django.db import models
# from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

class Alumno(models.Model):
    nombre = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    alumno_moodle_id = models.PositiveIntegerField(unique=True)
    foto_url = models.URLField(blank=True, null=True)
    foto_archivo = models.ImageField(upload_to='alumnos_fotos/', blank=True, null=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'alumnos'
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ['id']

class User(AbstractUser):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, blank=False, null=False)
    
    def __str__(self):
        # Always return something logic to the model in __str__, and never use .format, use fstring instead
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["id"]
