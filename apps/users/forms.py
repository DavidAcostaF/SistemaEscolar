from django import forms
from .models import User  # usa tu modelo extendido
from django.conf import settings
import requests
from django.contrib.auth.forms import AuthenticationForm


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

        self.alumno_moodle_id = data[0]['id']
        # self.objects.alumno_moodle_id = data[0]['username']
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.alumno_moodle_id = self.alumno_moodle_id
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
