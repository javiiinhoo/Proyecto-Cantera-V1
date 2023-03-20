import datetime
import io
from django.utils import timezone
from django.shortcuts import redirect, render
from .forms import BuscarJugadorForm
from .models import Jugador, Configuracion
from django.shortcuts import redirect
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import get_object_or_404, redirect, render
from app.models import Profile
from django.http import JsonResponse
import csv
from django.shortcuts import render, redirect
from .models import Jugador
from .forms import ImportarJugadoresForm, BuscarJugadorForm
from django.http import HttpResponse
from django.shortcuts import render
from app.models import Jugador
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import BuscarJugadorForm, LoginForm, ProfileForm, RegisterForm
from django.contrib.auth.models import User


def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def perfil(request, username):
    user = get_object_or_404(User, username=username)
    perfil_usuario = user.profile
    if request.user != user:
        return HttpResponse('No está autorizado para ver este perfil.')
    if request.method == 'POST':
        perfil_form = ProfileForm(
            request.POST, request.FILES, instance=perfil_usuario)
        if perfil_form.is_valid():
            perfil_form.save()
            messages.success(
                request, 'Se han guardado los cambios en el perfil')
            return redirect('perfil', username=username)
    else:
        perfil_form = ProfileForm(instance=perfil_usuario)
    context = {'perfil': perfil_usuario, 'perfil_form': perfil_form}
    return render(request, 'perfil.html', context)


def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'inicio_sesion.html', {'form': form})


@login_required
def adminpage(request): return render(request, 'adminpage.html')
def index(request): return render(request, 'index.html')


@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            request.user = form.save()
            messages.success(
                request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contraseña.html', {'form': form})


def cerrar_sesion(request): logout(request); return redirect('index')


@login_required
def eliminar_foto(request, username):
    print('Eliminando foto...')
    perfil = get_object_or_404(Profile, user__username=username)
    if request.method == 'POST':
        delete_photo = request.POST.get('delete_photo')
        if delete_photo:
            if perfil.photo:
                perfil.photo.delete()
                perfil.photo = 'default_profile_photo.png'
                messages.success(
                    request, 'La foto de perfil ha sido eliminada.')
                perfil.save()
                return redirect('perfil', username=username)
        perfil_form = ProfileForm(request.POST, request.FILES, instance=perfil)
        if perfil_form.is_valid():
            perfil = perfil_form.save(commit=False)
            perfil.save()
            messages.success(
                request, 'La información de perfil ha sido actualizada.')
            return redirect('perfil', username=username)
    else:
        perfil_form = ProfileForm(instance=perfil)
    return render(request, 'perfil.html', {'perfil_form': perfil_form, 'perfil': perfil})


def importar_jugadores(request):
    if request.method == 'POST':
        form = ImportarJugadoresForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            header = ['Nombre Jugador', 'Enlace TM', 'Temporada', 'Fecha',
                      'Último club', 'Nuevo club', 'Valor de mercado', 'Coste']
            try:
                archivo_str = archivo.read().decode('utf-8')
                print('Contenido del archivo CSV:', archivo_str)
                reader = csv.reader(io.StringIO(archivo_str), delimiter=',')
                header_csv = next(reader)
                print('Cabecera del archivo CSV:', header_csv)
                if header_csv != header:
                    form.add_error(
                        'archivo', 'El archivo debe tener las columnas correctas')
                else:
                    jugadores = []
                    for row in reader:
                        jugador = Jugador(nombre=row[0], enlace=row[1], temporada=row[2], fecha=row[3],
                                          ultimo_club=row[4], nuevo_club=row[5], valor_mercado=row[6], coste=row[7])
                        jugadores.append(jugador)
                    try:
                        Jugador.objects.bulk_create(jugadores)
                    except Exception as e:
                        print('Error al guardar los datos en la base de datos:', e)
                        form.add_error(
                            'archivo', 'Error al guardar los datos en la base de datos')
                    configuracion = Configuracion(
                        ultima_importacion=datetime.datetime.now())
                    configuracion.save()
                    messages.success(
                        request, 'Los jugadores se han importado correctamente.')
                    return redirect('buscar_jugador')
            except Exception as e:
                form.add_error('archivo', 'Error al procesar el archivo')
                messages.error(
                    request, f"Ocurrió un error al procesar el archivo: {e}")
        else:
            print('form.errors:', form.errors)
    else:
        form = ImportarJugadoresForm()
    context = {'form': form}
    return render(request, 'importar_jugadores.html', context)


def buscar_jugador(request):
    jugadores = []
    jugadores_en_bd = Jugador.objects.all()
    if not jugadores_en_bd:
        messages.warning(
            request, 'No se encontraron jugadores en la base de datos. Por favor, importe los jugadores.')
        return redirect('importar_jugadores')
    if request.method == 'POST':
        form = BuscarJugadorForm(request.POST)
        if form.is_valid():
            nombre_jugador = form.cleaned_data['nombre']
            jugadores = Jugador.objects.filter(
                nombre__icontains=nombre_jugador)
            if not jugadores:
                messages.warning(
                    request, 'No se encontraron jugadores con ese nombre.')
            else:
                return redirect('lista_jugadores', query=nombre_jugador)
    else:
        form = BuscarJugadorForm()
    configuracion = Configuracion.objects.first()
    if not configuracion:
        messages.success(
            request, 'No se encontró ninguna configuración. Por favor, importe los jugadores.')
        return redirect('importar_jugadores')
    if configuracion.ultima_importacion < timezone.now()-timezone.timedelta(weeks=6):
        messages.success(
            request, 'La última importación se realizó hace más de 6 semanas. Por favor, importe los jugadores.')
        return redirect('importar_jugadores')
    return render(request, 'buscar_jugador.html', {'form': form, 'jugadores': jugadores})


def lista_jugadores(request, query=None):
    if query:
        jugadores = Jugador.objects.filter(nombre__icontains=query)
    else:
        jugadores = Jugador.objects.all()
    return render(request, 'lista_jugadores.html', {'jugadores': jugadores})
