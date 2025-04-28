from django.db import models
from django.db import models
from apps.materias.models import Materia
from apps.users.models import Alumno

# Create your models here.
class Tarea(models.Model):
    nombre = models.CharField(max_length=255)
    moodle_id = models.PositiveIntegerField(unique=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.TextField(blank=True, null=True)
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    parcial = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.materia.nombre})"
    
    class Meta:
        db_table = 'tareas'
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['id']


class TareaAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='tareas_alumno')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='alumnos_tarea')
    calificacion = models.FloatField(blank=True, null=True)
    entregada = models.BooleanField(default=False)
    fecha_entrega_real = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('alumno', 'tarea')
        db_table = 'tareas_alumnos'
        verbose_name = "Tarea Alumno"
        verbose_name_plural = "Tareas Alumnos"

    def __str__(self):
        return f"{self.alumno} - {self.tarea}"
