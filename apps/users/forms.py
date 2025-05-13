from django import forms
from .models import User  # usa tu modelo extendido
from django.conf import settings
import requests
from django.contrib.auth.forms import AuthenticationForm
from .models import Alumno

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


    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        moodle_username = self.cleaned_data.get('alumno_moodle')
        alumno = Alumno.objects.filter(username=moodle_username).first()

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if not alumno:
            raise forms.ValidationError("El username de Moodle no existe.")
        
        self.alumno_moodle = alumno

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        self.alumno = self.alumno_moodle
        # user.alumno_moodle_id = self.alumno_moodle_id
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
