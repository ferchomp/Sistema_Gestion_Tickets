"""
Definición del modelo de Usuario utilizando MongoDB y MongoEngine.
"""

import mongoengine as me  # 📌 Importamos MongoEngine para definir los modelos en MongoDB
from datetime import datetime  # 📌 Importamos datetime para manejar fechas

class Usuario(me.Document): 
    """
    Modelo de Usuario para autenticación y gestión en MongoDB.
    """
    
    # 📌 Nombre de usuario, debe ser único y con un máximo de 150 caracteres
    username = me.StringField(required=True, unique=True, max_length=150)
    
    # 📌 Correo electrónico del usuario, debe ser único
    email = me.EmailField(required=True, unique=True)
    
    # 📌 Contraseña del usuario, almacenada de forma encriptada
    password = me.StringField(required=True)
    
    # 📌 Rol del usuario (puede ser "agente" o "solicitante"), con "solicitante" como valor predeterminado
    rol = me.StringField(choices=["agente", "solicitante"], default="solicitante")
    
    # 📌 Fecha de creación del usuario (se asigna automáticamente al momento de la creación)
    created_at = me.DateTimeField(default=datetime.utcnow)
    
    # 📌 Fecha de última actualización (se actualiza automáticamente cada vez que el documento cambia)
    updated_at = me.DateTimeField(default=datetime.utcnow, auto_now=True)

    # 📌 Especificamos la colección donde se almacenará este modelo en MongoDB
    meta = {'collection': 'usuarios'}

    USERNAME_FIELD = "username"  # 📌 Campo principal de autenticación

    def is_authenticated(self):
        """
        Método necesario para que Django reconozca este modelo como usuario autenticado.
        """
        return True

    def __str__(self):
        return self.username