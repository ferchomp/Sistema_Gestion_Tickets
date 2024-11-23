from django.db import models

# Create your models here.
from mongoengine import Document, StringField,  DateTimeField, ReferenceField, FileField

class Ticket(Document):
    asignado = StringField(required=True)  # Asignado a
    solicitante = StringField(required=True)  # Solicitante
    departamento = StringField(required=True)  # Departamento del solicitante
    fecha_creacion = DateTimeField(required=True) # Fecha de creación
    asunto = StringField(required=True)  # Asunto del ticket
    descripcion = StringField(required=True)  # Descripción del problema
    tipo_ticket = StringField(choices=["Incidente", "Problema", "Solicitud de servicio", "Consulta"], required=True)  # Tipo de ticket
    estado_ticket = StringField(choices=["Abierto", "Cerrado", "Proceso"], required=True)  # Estado del ticket
    prioridad = StringField(choices=["Urgente", "Alta", "Media", "Baja"], required=True)  # Prioridad del ticket
    fecha_resolucion =  DateTimeField()  # Fecha de resolución (opcional)
    adjunto = FileField()  # Archivo adjunto (opcional)

    def __str__(self):
        return f"{self.asunto} - {self.solicitante}"

