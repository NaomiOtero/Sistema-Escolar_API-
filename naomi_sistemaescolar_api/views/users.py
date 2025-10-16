import json
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

class Userme(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        #TODO: Regresar perfil del usuario
        return Response({})

class AdminView(generics.CreateAPIView):
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # Serializamos los datos del administrador para volverlo de nuevo JSON
        user = UserSerializer(data=request.data)
        
        if user.is_valid():
            #Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1) #Activo por default


            user.save()
            #Cifrar la contraseña
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            #Almacenar los datos adicionales del administrador
            admin = Administradores.objects.create(user=user,
                                            clave_admin= request.data["clave_admin"],
                                            telefono= request.data["telefono"],
                                            rfc= request.data["rfc"].upper(),
                                            edad= request.data["edad"],
                                            ocupacion= request.data["ocupacion"])
            admin.save()

            return Response({"admin_created_id": admin.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AlumnosView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)  # Puedes cambiar esto si necesitas autenticación

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

            return Response({"student_created_id": alumno.id}, status=status.HTTP_201_CREATED)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MaestroView(generics.CreateAPIView):
       #Registrar nuevo usuario
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
                     return Response({"message":"Username "+email+", is already taken"},400)
            
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

                # Crear registro en tabla Maestros
                maestro = Maestros.objects.create(user=user,
                                            id_maestro=request.data["id_maestro"],
                                            fecha_nacimiento=request.data["fecha_nacimiento"],
                                            telefono=request.data["telefono"],
                                            rfc=request.data["rfc"].upper(),
                                            cubiculo=request.data["cubiculo"],
                                            area_investigacion=request.data["area_investigacion"],
                                            materias_json= json.dumps(request.data["materias_json"]))
                
                maestro.save()

                return Response({"teacher_created_id": maestro.id}, 201)

            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
