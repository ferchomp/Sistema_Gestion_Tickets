from django.db import models

# Create your models here.
from mongoengine import Document, StringField

class Departamento(Document):
    nombre = StringField(required=True, unique=True)

    def __str__(self):
        return self.nombre
