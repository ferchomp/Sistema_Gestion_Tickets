# usuarios/serializers.py

from rest_framework import serializers
from .models import Usuario 

class UsuarioSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # Crear el usuario en MongoDB
        return Usuario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Actualizar los campos del usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
