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
import json

class MaestrosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        #TODO: Regresar perfil del usuario
        return Response({})
    
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
