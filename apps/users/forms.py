from django import forms
from .models import User  # usa tu modelo extendido
from django.conf import settings
import requests
class RegisterForm(forms.ModelForm):
    alumno_moodle = forms.CharField(label='Username de moodle')

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}),
    )

    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Crear Usuario',
        }

        help_texts = {
            'username': None,
        }

    def clean_alumno_moodle(self):
        username = self.cleaned_data['alumno_moodle']

        url = settings.MOODLE_API_URL
        params = {
            'wstoken': settings.MOODLE_TOKEN,
            'wsfunction': 'core_user_get_users_by_field',
            'moodlewsrestformat': 'json',
            'field': 'username',
            'values[0]': username
        }

        response = requests.get(url, params=params)
        data = response.json()
        print("Usuario de moodle",data)
        if not data:
            raise forms.ValidationError("El usuario no fue encontrado en Moodle.")

        # Guardamos el ID encontrado en una variable interna temporal
        self.moodle_user_id = data[0]['id']
        return username
