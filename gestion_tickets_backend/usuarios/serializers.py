"""
Serializadores para el modelo Usuario en MongoDB.
"""

import re  # 📌 Importamos el módulo de expresiones regulares para validar contraseñas
from rest_framework import serializers  # 📌 Importamos el serializador de Django REST Framework
import bcrypt  # 📌 Para el cifrado seguro de contraseñas
from .models import Usuario  # 📌 Importamos nuestro modelo de usuario

class UsuarioSerializer(serializers.Serializer):
    """
    Serializador para manejar datos del usuario en la API.
    """

    # 📌 Convertimos el ObjectId de MongoDB a string para evitar errores
    id = serializers.SerializerMethodField()
    
    # 📌 Campos de usuario
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    
    # 📌 La contraseña solo se escribe en la solicitud, pero no se devuelve en la respuesta
    password = serializers.CharField(write_only=True)
    
    # 📌 Definimos el rol del usuario con opciones "agente" o "solicitante"
    rol = serializers.ChoiceField(choices=["agente", "solicitante"], default="solicitante")

    def get_id(self, obj):
        """
        Convierte el ObjectId de MongoDB a string.
        """
        return str(obj.id)

    def validate_password(self, value):
        """
        Valida que la contraseña cumpla con los requisitos de seguridad.
        """
        
        # 📌 Verificamos que tenga al menos 8 caracteres
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        # 📌 Requerimos al menos una letra mayúscula
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Debe incluir al menos una letra mayúscula.")

        # 📌 Requerimos al menos un número
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Debe incluir al menos un número.")

        return value

    def create(self, validated_data):
        """
        Crea un usuario con la contraseña cifrada.
        """

        # 📌 Ciframos la contraseña con bcrypt
        validated_data["password"] = bcrypt.hashpw(
            validated_data["password"].encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

        # 📌 Normalizamos el rol a minúsculas
        validated_data["rol"] = validated_data["rol"].lower()

        # 📌 Creamos y guardamos el usuario en la base de datos
        usuario = Usuario(**validated_data)
        usuario.save()

        return usuario

    def update(self, instance, validated_data):
        """
        Actualiza datos del usuario, encriptando la nueva contraseña si se cambia.
        """

        if "password" in validated_data:
            validated_data["password"] = bcrypt.hashpw(
                validated_data["password"].encode('utf-8'), bcrypt.gensalt()
            ).decode('utf-8')  # 📌 Hasheamos la nueva contraseña si se cambia

        # 📌 Asignamos los valores actualizados al objeto del usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 📌 Guardamos los cambios en la base de datos
        instance.save()

        return instance
