from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Saldo
from usuarios.models import Usuario
from bson import ObjectId  # Import necesario para manejar ObjectId de MongoDB

class ConsultarSaldoView(APIView):
    def get(self, request, usuario_id):
        # Verifica que el usuario_id sea un ObjectId válido
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Buscar usuario por el _id
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Buscar el saldo asociado al usuario
        saldo = Saldo.objects.filter(usuario=usuario).first()
        if saldo:
            return Response({"usuario": usuario_id, "saldo_actual": saldo.saldo_actual}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Saldo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class ActualizarSaldoView(APIView):
    def post(self, request, usuario_id):
        # Verifica que el usuario_id sea un ObjectId válido
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Buscar usuario por el _id
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        if 'cambio_saldo' not in data:
            return Response({"error": "Se requiere el campo 'cambio_saldo'"}, status=status.HTTP_400_BAD_REQUEST)
        
        cambio_saldo = data['cambio_saldo']

        # Buscar o crear el saldo asociado al usuario
        saldo = Saldo.objects.filter(usuario=usuario).first()
        if not saldo:
            saldo = Saldo(usuario=usuario, saldo_actual=0.0)  # Crear saldo inicial
        
        # Actualizar el saldo actual
        saldo.saldo_actual += cambio_saldo
        saldo.save()  # Guardar cambios en la base de datos
        
        return Response({"usuario": usuario_id, "nuevo_saldo": saldo.saldo_actual}, status=status.HTTP_200_OK)
