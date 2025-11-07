from django.db.models import *
from django.db import transaction
from naomi_sistemaescolar_api.serializers import UserSerializer
from naomi_sistemaescolar_api.serializers import *
from naomi_sistemaescolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group


class AlumnosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active=1).order_by('id')
        lista = AlumnoSerializer(alumnos, many=True).data
        
        return Response(lista, 200)
    
class AlumnosView(generics.CreateAPIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user = UserSerializer(data=request.data)
        if user.is_valid():
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']

            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message": "El correo ya está registrado"}, status=status.HTTP_400_BAD_REQUEST)

            # Crear usuario base
            user = User.objects.create( username=email,
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name,
                                        is_active=1)  # Activo por defecto

            user.save()
            user.set_password(password)
            user.save()

            # Asignar grupo
            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            # Crear registro en tabla Alumnos
            alumno = Alumnos.objects.create(user=user,
                                            matricula=request.data["matricula"],
                                            fecha_nacimiento=request.data["fecha_nacimiento"],
                                            curp=request.data["curp"].upper(),
                                            rfc=request.data["rfc"].upper(),
                                            edad=request.data["edad"],
                                            telefono=request.data["telefono"],
                                            ocupacion=request.data["ocupacion"])
            
            alumno.save()

            return Response({"ALumno creado con iD": alumno.id}, status=status.HTTP_201_CREATED)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)