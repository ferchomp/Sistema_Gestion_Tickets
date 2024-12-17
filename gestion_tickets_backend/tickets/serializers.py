from rest_framework import serializers
from .models import Ticket  # Importamos el modelo Ticket

class TicketSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoEngine usa un id tipo string
    asignado = serializers.CharField()
    solicitante = serializers.CharField()
    departamento = serializers.CharField()
    fecha_creacion = serializers.DateTimeField()
    asunto = serializers.CharField()
    descripcion = serializers.CharField()
    tipo_ticket = serializers.CharField()
    estado_ticket = serializers.CharField()
    prioridad = serializers.CharField()
    fecha_resolucion = serializers.DateTimeField(allow_null=True, required=False)

    def create(self, validated_data):
        """
        Crea un nuevo ticket en la base de datos.
        """
        return Ticket(**validated_data).save()

    def update(self, instance, validated_data):
        """
        Actualiza un ticket existente.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
