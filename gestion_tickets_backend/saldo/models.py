# models.py de la aplicación 'saldo'
from mongoengine import Document, ReferenceField, FloatField, DateTimeField
from django.utils.timezone import now
from usuarios.models import Usuario  

class Saldo(Document):
    usuario = ReferenceField(Usuario, required=True)  # Relación con el modelo Usuario
    saldo_actual = FloatField(default=0.0)  # Saldo actual del usuario, valor por defecto 0.0
    fecha_actualizacion = DateTimeField(default=now)  # Fecha y hora de la última actualización del saldo

    meta = {
        'collection': 'saldo',  # Nombre de la colección en MongoDB
        'ordering': ['-fecha_actualizacion']  # Ordenar por la fecha de actualización, de más reciente a más antiguo
    }
