from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Jugador
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    delete_photo = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['direccion', 'telefono', 'photo']
        widgets = {'direccion': forms.TextInput(attrs={'class': 'form-control'}), 'telefono': forms.TextInput(
            attrs={'class': 'form-control'}), 'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'})}

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        delete_photo = self.cleaned_data.get('delete_photo', False)
        print('e')
        if delete_photo:
            if photo:
                photo.delete()
            return None
        if photo:
            if photo.size > 2*1024*1024:
                raise ValidationError(
                    _('El tamaño de la imagen no debe ser mayor a 2MB'))
            if not photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError(
                    _('Formato de archivo no válido. Los formatos aceptados son JPG, JPEG y PNG.'))
        return photo


class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class ImportarJugadoresForm(forms.Form):
    archivo = forms.FileField()

    class Meta:
        widgets = {'archivo': forms.ClearableFileInput(
            attrs={'multiple': True})}

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if archivo:
            extension = archivo.name.split('.')[-1]
            if extension != 'csv':
                raise forms.ValidationError(
                    'El archivo debe ser un archivo CSV')
        return archivo


class BuscarJugadorForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200)

    class Meta:
        model = Jugador
        fields = ['nombre']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, required=True, widget=forms.EmailInput())
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']
        labels = {'username': 'Nombre de usuario', 'email': 'Correo electrónico', 'first_name': 'Nombre',
                  'last_name': 'Apellido', 'password1': 'Contraseña', 'password2': 'Confirmar contraseña'}


class CambiarContraseñaForm(forms.Form):
    password_actual = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    password_nuevo = forms.CharField(
        label='Contraseña nueva',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    password_confirmacion = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not authenticate(
            username=self.user.username,
            password=password_actual
        ):
            raise forms.ValidationError('Contraseña actual incorrecta')
        return password_actual

    def clean(self):
        cleaned_data = super().clean()
        password_nuevo = cleaned_data.get('password_nuevo')
        password_confirmacion = cleaned_data.get('password_confirmacion')
        if password_nuevo != password_confirmacion:
            raise forms.ValidationError(
                'Las contraseñas nuevas no coinciden'
            )
        if password_nuevo == self.cleaned_data.get('password_actual'):
            raise forms.ValidationError(
                'La contraseña nueva no puede ser igual a la actual'
            )
        return cleaned_data


class SolicitudVerificacionForm(forms.Form):
    nombres = forms.CharField(label="Nombres", max_length=255)
    apellidos = forms.CharField(label="Apellidos", max_length=255)
    perfil = forms.CharField(label="Perfil", max_length=10)
    foto_perfil = forms.ImageField(label="Foto de perfil")
