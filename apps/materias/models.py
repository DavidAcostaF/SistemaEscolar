# apps/materias/models.py

from django.db import models
from apps.users.models import Alumno

class Materia(models.Model):
    nombre = models.CharField(max_length=255)
    moodle_id = models.PositiveIntegerField(unique=True)
    etiqueta = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'materias'
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['id']


class MateriaAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='materias_alumno')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='alumnos_materia')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'materias_alumnos'
        unique_together = ('alumno', 'materia')  # No duplicar registros
        verbose_name = "Materia Alumno"
        verbose_name_plural = "Materias Alumnos"

    def __str__(self):
        return f"{self.alumno} en {self.materia}"
