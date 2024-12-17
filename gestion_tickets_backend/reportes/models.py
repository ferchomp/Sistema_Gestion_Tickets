# models.py
from mongoengine import Document, ReferenceField, DateTimeField, StringField
from tickets.models import Ticket  # Importar el modelo Ticket

class Reporte(Document):
    ticket = ReferenceField(Ticket, required=True)  # Relación con el modelo Ticket
    fecha = DateTimeField(required=True)
    estado_ticket = StringField(required=True, max_length=50)
    asignado = StringField(required=True, max_length=100)

    def __str__(self):
        return f"Reporte de Ticket {self.ticket.id} - {self.estado_ticket}"
