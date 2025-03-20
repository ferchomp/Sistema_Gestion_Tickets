from mongoengine import Document, StringField, DateTimeField, ReferenceField
from django.utils import timezone
from usuarios.models import Usuario  # Importa el modelo de usuarios (si está en MongoEngine)

class Ticket(Document):
    asignado = ReferenceField(Usuario, required=False, null=True)  # Si Usuario está en MongoEngine
    solicitante = StringField(required=True, max_length=100)
    departamento = StringField(required=True, max_length=100)
    fecha_creacion = DateTimeField(default=timezone.now)
    asunto = StringField(required=True, max_length=200)
    descripcion = StringField(required=True)
    tipo_ticket = StringField(choices=["Incidente", "Problema", "Solicitud de servicio", "Consulta"], required=True)
    estado_ticket = StringField(choices=["Abierto", "Cerrado", "Proceso"], required=True, default="Abierto")
    prioridad = StringField(choices=["Urgente", "Alta", "Media", "Baja"], required=True)
    fecha_resolucion = DateTimeField(null=True)  # Se permite que no tenga valor inicial
    archivo = StringField(null=True)  # Guarda la ruta del archivo si se sube uno

    def __str__(self):
        return f"Ticket: {self.asunto} - Solicitante: {self.solicitante}"
