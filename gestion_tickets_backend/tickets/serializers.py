from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.Serializer):
    solicitante = serializers.CharField(max_length=100)
    departamento = serializers.CharField(max_length=100)
    fecha_creacion = serializers.DateTimeField(required=False)
    asunto = serializers.CharField(max_length=200)
    descripcion = serializers.CharField()
    tipo_ticket = serializers.ChoiceField(choices=["Incidente", "Problema", "Solicitud de servicio", "Consulta"])
    prioridad = serializers.ChoiceField(choices=["Urgente", "Alta", "Media", "Baja"])
    estado_ticket = serializers.ChoiceField(choices=["Abierto", "En proceso", "Cerrado"], required=False)
    fecha_resolucion = serializers.SerializerMethodField()

    def get_fecha_resolucion(self, obj):
        """Convierte `datetime` en `date` para evitar el error de formato"""
        return obj.fecha_resolucion.date() if obj.fecha_resolucion else None

    def create(self, validated_data):
        ticket = Ticket(**validated_data)
        ticket.save()
        return ticket

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        instance.reload()
        return instance