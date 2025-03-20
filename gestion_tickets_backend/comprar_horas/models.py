# models.py de la aplicación 'comprar_horas'
from mongoengine import Document, ReferenceField, FloatField, IntField, DateTimeField
from django.utils.timezone import now
from usuarios.models import Usuario

class CompraHoras(Document):
    usuario = ReferenceField(Usuario, required=True)  # Usuario que compra las horas
    horas_compradas = IntField(required=True)  # Número de horas compradas
    precio_por_hora = FloatField(required=True)  # Precio por hora
    monto_total = FloatField(required=True)  # Monto total de la compra
    fecha_compra = DateTimeField(default=now)  # Fecha en que se realizó la compra

    meta = {
        'collection': 'compras_horas',
        'ordering': ['-fecha_compra']  # Ordenar las compras por fecha (más recientes primero)
    }
