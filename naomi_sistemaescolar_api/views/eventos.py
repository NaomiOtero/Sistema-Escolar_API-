from django.db import transaction
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from naomi_sistemaescolar_api.serializers import EventosSerializer
from naomi_sistemaescolar_api.models import Eventos
import json


class EventosAll(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventosSerializer

    def get_queryset(self):
        return Eventos.objects.filter(user__is_active=1).order_by("id")

    def list(self, request, *args, **kwargs):
        eventos = self.get_queryset()
        data = EventosSerializer(eventos, many=True).data

        # Convertir JSON almacenado como texto a listas
        for evento in data:
            if "objetivo_json" in evento and evento["objetivo_json"]:
                try:
                    evento["objetivo_json"] = json.loads(evento["objetivo_json"])
                except:
                    evento["objetivo_json"] = []

        return Response(data, status=200)


class EventosView(generics.CreateAPIView):
    serializer_class = EventosSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [] 
        return [permissions.IsAuthenticated()]

    # Obtener evento por ID
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        data = EventosSerializer(evento).data

        # Cargar JSON
        try:
            data["objetivo_json"] = json.loads(data["objetivo_json"])
        except:
            data["objetivo_json"] = []

        return Response(data, status=200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # El usuario autenticado es el que crea el evento
        user = request.user  

        evento = Eventos.objects.create(
            user = user,
            name_event = request.data["name_event"],
            tipo_evento = request.data["tipo_evento"],
            fecha = request.data["fecha"],
            hora_inicio = request.data["hora_inicio"],
            hora_final = request.data["hora_final"],
            lugar = request.data["lugar"],
            objetivo_json = json.dumps(request.data["objetivo_json"]),
            programa_educativo = request.data["programa_educativo"],
            responsable_evento = request.data["responsable_evento"],
            descripcion = request.data["descripcion"],
            Asistentes = request.data["Asistentes"]
        )

        return Response({"evento_created_id": evento.id }, status=201)


    # Actualizar evento
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.data["id"])
        data = request.data.copy()

        # Convertir JSON antes de guardar
        if "objetivo_json" in data:
            data["objetivo_json"] = json.dumps(data["objetivo_json"])

        serializer = EventosSerializer(evento, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Evento actualizado correctamente"}, status=200)

        return Response(serializer.errors, status=400)

    # Eliminar evento
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))

        try:
            evento.delete()
            return Response({"details": "Evento eliminado"}, status=200)
        except:
            return Response({"details": "Error al eliminar"}, status=400)
        
class TotalEventos(generics.CreateAPIView):

    def get(self, request, *args, **kwargs):
        eventos_qs = Eventos.objects.filter(user__is_active=True)

        total_estudiantes = 0
        total_profesores = 0
        total_publico = 0

        for e in eventos_qs:
            # e.objetivo_json viene como str en la BD (JSON serializado)
            try:
                objetivos = json.loads(e.objetivo_json)
            except:
                objetivos = []

            # objetivos es ahora una lista: ["1"], ["2"], ["1","3"], etc.
            for objetivo in objetivos:
                tipo = str(objetivo)  # convertir cada elemento a string
                if tipo == "Estudiantes":
                    total_estudiantes += 1
                elif tipo == "Profesores":
                    total_profesores += 1
                elif tipo == "Publico General":
                    total_publico += 1

        return Response(
            {
                "estudiantes": total_estudiantes,
                "profesores": total_profesores,
                "publico": total_publico
            },
            status=200
        )
