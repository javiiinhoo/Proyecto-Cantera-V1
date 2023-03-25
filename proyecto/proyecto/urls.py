from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [path('', views.index, name='index'), path('registro/', views.registro, name='registro'), path('aprobacion_registro/', views.aprobacion_registro, name='aprobacion_registro'), path('lista_jugadores/<str:query>/', views.lista_jugadores, name='lista_jugadores'), path('perfil/<str:username>/', views.perfil, name='perfil'), path('perfil/<str:username>/eliminar_foto/', views.eliminar_foto, name='eliminar_foto'), path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'), path('solicitar_verificacion/',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                views.solicitar_verificacion, name='solicitar_verificacion'), path('logout/', views.cerrar_sesion, name='logout'), path('cambiar_contraseña/', auth_views.PasswordChangeView.as_view(template_name='cambiar_contraseña.html', success_url='/'), name='cambiar_contraseña'), path('importar_jugadores/', views.importar_jugadores, name='importar_jugadores'), path('buscar_jugador/', views.buscar_jugador, name='buscar_jugador'), path('admin/', admin.site.urls)]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATICFILES_DIRS)
