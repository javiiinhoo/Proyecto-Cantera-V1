from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Func


class Unaccent(Func):
    function = 'UNACCENT'


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    enlace = models.URLField()
    temporada = models.CharField(max_length=10)
    fecha = models.CharField(max_length=20)
    ultimo_club = models.CharField(max_length=100)
    nuevo_club = models.CharField(max_length=100)
    valor_mercado = models.CharField(max_length=20)
    coste = models.CharField(max_length=20)
    def __str__(self): return self.nombre


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos',
                              blank=True, null=True, default='default_profile_photo.png')
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    aprobado = models.BooleanField(default=False)
    def __str__(self): return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, aprobado=False)


class Configuracion(models.Model):
    ultima_importacion = models.DateTimeField(default=timezone.now)


class SolicitudVerificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField()

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'Solicitud de verificación de {self.user.username}'
