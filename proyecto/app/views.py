from app.models import Jugador
import csv
from .forms import BuscarJugadorForm
from .models import Jugador
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vista_protegida')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'inicio_sesion.html', {'form': form})


@login_required
def adminpage(request):
    return render(request, 'adminpage.html')


def index(request):
    return render(request, 'index.html')


@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contraseña.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('index')


def buscar_jugador(request):
    if request.method == 'POST':
        form = BuscarJugadorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            jugadores = Jugador.objects.filter(nombre__icontains=nombre)
            if jugadores.exists():
                return render(request, 'jugadores_encontrados.html', {'jugadores': jugadores})
            else:
                return render(request, 'jugador_no_encontrado.html')
    else:
        form = BuscarJugadorForm()
    return render(request, 'buscar_jugador.html', {'form': form})


def importar_jugadores(request):
    if request.method == 'POST' and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        jugadores = csv.DictReader(archivo)
        for jugador in jugadores:
            Jugador.objects.create(
                nombre=jugador['nombre'],
                enlace=jugador['enlace'],
                temporada=jugador['temporada'],
                fecha=jugador['fecha'],
                ultimo_club=jugador['ultimo_club'],
                nuevo_club=jugador['nuevo_club'],
                valor_mercado=jugador['valor_mercado'],
                coste=jugador['coste']
            )

        return redirect('lista_jugadores')
    return render(request, 'importar_jugadores.html')
