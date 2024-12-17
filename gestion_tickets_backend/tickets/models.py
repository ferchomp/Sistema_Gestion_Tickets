from mongoengine import Document, StringField, DateTimeField, ReferenceField
from django.utils import timezone  # Para obtener la fecha y hora actual con zona horaria



class Ticket(Document):
    # Campo que indica quién está asignado para resolver el ticket (nombre de la persona o equipo)
    asignado = StringField(required=True, max_length=100)  # Asignado a
    
    # Campo que indica el nombre de la persona que solicita el soporte
    solicitante = StringField(required=True, max_length=100)  # Nombre del solicitante
    
    # Campo para indicar el departamento del solicitante (por ejemplo, TI, Recursos Humanos, etc.)
    departamento = StringField(required=True, max_length=100)  # Departamento del solicitante
    
    # Campo para la fecha de creación del ticket, con valor por defecto de la fecha actual
    fecha_creacion = DateTimeField(default=timezone.now)  # Fecha de creación, con valor por defecto
    
    # Campo para el asunto o título del ticket (lo que describe brevemente el problema)
    asunto = StringField(required=True, max_length=200)  # Asunto del ticket
    
    # Campo para una descripción más detallada del problema que está experimentando el solicitante
    descripcion = StringField(required=True)  # Descripción del problema
    
    # Campo para el tipo de ticket, con opciones predefinidas
    tipo_ticket = StringField(
        choices=["Incidente", "Problema", "Solicitud de servicio", "Consulta"], 
        required=True
    )  # Tipo de ticket
    
    # Campo para el estado del ticket, con opciones predefinidas
    estado_ticket = StringField(
        choices=["Abierto", "Cerrado", "Proceso"], 
        required=True
    )  # Estado del ticket
    
    # Campo para la prioridad del ticket, con opciones predefinidas
    prioridad = StringField(
        choices=["Urgente", "Alta", "Media", "Baja"], 
        required=True
    )  # Prioridad del ticket
    
    # Campo para la fecha de resolución del ticket, que puede ser nulo si el ticket aún no se ha resuelto
    fecha_resolucion = DateTimeField(null=True)  # Fecha de resolución (opcional)

    # Método especial para representar el ticket como un string
    def __str__(self):
        return f"Ticket: {self.asunto} - Solicitante: {self.solicitante}"
