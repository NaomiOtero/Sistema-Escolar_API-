from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from naomi_sistemaescolar_api.views import bootstrap
from naomi_sistemaescolar_api.views import users
from naomi_sistemaescolar_api.views import alumnos
from naomi_sistemaescolar_api.views import maestro
from naomi_sistemaescolar_api.views import auth

urlpatterns = [
    #crear admin
        path('admin/', users.AdminView.as_view()),
    #admin data
        path('Lista-admins/', users.AdminAll.as_view()),
    #Edit Admin
       # path('admins_edit/', users.AdminViewEdit.as_view()),

       #crear admin
        path('alumno/', alumnos.AlumnosView.as_view()),
    #admin data
        path('Lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Edit Admin
       # path('admins_edit/', alumnos.AlumnosViewEdit.as_view()),

       #crear admin
        path('maestro/', maestro.MaestroView.as_view()),
    #admin data
        path('Lista-maestros/', maestro.MaestrosAll.as_view()),
    #Edit Admin
       # path('admins_edit/', maestro.MaestroViewEdit.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
