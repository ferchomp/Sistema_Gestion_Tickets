# gestion_tickets_backend/users/models.py

from mongoengine import Document, StringField, EmailField

class User(Document):
    username = StringField(required=True, unique=True)  # Nombre de usuario único
    password = StringField(required=True)                # Contraseña del usuario
    email = EmailField(required=True, unique=True)      # Correo electrónico único
    rol = StringField(choices=["Técnico", "Solicitante"])
    

    def __str__(self):
        return self.username  # Representación del modelo como cadena