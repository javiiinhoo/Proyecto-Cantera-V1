
from .models import Jugador
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class BuscarJugadorForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200)

    class Meta:
        model = Jugador
        fields = ['nombre']
