# gestion_tickets_backend/usuarios/models.py

from mongoengine import Document, StringField, EmailField

class Usuario(Document):
    username = StringField(required=True, unique=True)  # Nombre de usuario único
    password = StringField(required=True)                # Contraseña del usuario
    email = EmailField(required=True, unique=True)      # Correo electrónico único
    rol = StringField(choices=["Técnico", "Solicitante"])
    

    def __str__(self):
        return self.username  # Representación del modelo como cadena

