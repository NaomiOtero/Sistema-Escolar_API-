from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from naomi_sistemaescolar_api.views import bootstrap, eventos
from naomi_sistemaescolar_api.views import users
from naomi_sistemaescolar_api.views import alumnos
from naomi_sistemaescolar_api.views import maestro
from naomi_sistemaescolar_api.views import auth

urlpatterns = [
    #Create Admin
        path('admin/', users.AdminView.as_view()),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Create Alumno
        path('alumnos/', alumnos.AlumnosView.as_view()),
    #Lista Alumnos
        path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Create Maestro
        path('maestros/', maestro.MaestrosView.as_view()),
        #Lista Maestros
        path('lista-maestros/', maestro.MaestrosAll.as_view()),
    #Login
        path('login/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),
    #total usarios
        #Total Users
        path('total-usuarios/', users.TotalUsers.as_view()),
    #total eventos
        #Total Eventos
        path('total-eventos/', eventos.TotalEventos.as_view()),
    #links para eventos 
    #Create Evento
        path('eventos/', eventos.EventosView.as_view()),
        #Lista Eventos
        path('lista-eventos/', eventos.EventosAll.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
