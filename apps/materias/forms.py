from django import forms

class SeleccionarAlumnoForm(forms.Form):
    alumno_id = forms.IntegerField(label='ID del Alumno', required=True)
