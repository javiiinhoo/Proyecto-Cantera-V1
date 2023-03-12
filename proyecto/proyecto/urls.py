from django.urls import path
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', auth_views.LoginView.as_view(
        template_name='inicio_sesion.html'), name='inicio_sesion'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('cambiar_contraseña/', auth_views.PasswordChangeView.as_view(
        template_name='cambiar_contraseña.html', success_url='/'), name='cambiar_contraseña'),
    path('importar_jugadores/', views.importar_jugadores,
         name='importar_jugadores'),
    path('buscar_jugadores/', views.buscar_jugador,
         name='buscar_jugadores'),
    path('importar_jugadores/', views.importar_jugadores,
         name='importar_jugadores'),
    path('importar_jugadores/', views.importar_jugadores,
         name='importar_jugadores'),

]
