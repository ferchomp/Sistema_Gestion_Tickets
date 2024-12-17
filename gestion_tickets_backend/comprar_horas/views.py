from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist, ValidationError
from .models import CompraHoras
from usuarios.models import Usuario


class ComprarHorasView(APIView):
    """
    Vista para comprar horas.
    """
    def post(self, request, usuario_id):
        """
        Permite a un usuario comprar un número específico de horas.
        :param usuario_id: ID del usuario que está realizando la compra
        :return: Response con la información de la compra
        """
        try:
            # Obtener el usuario por su ID (MongoEngine)
            usuario = Usuario.objects.get(id=usuario_id)
        except DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data

        # Validación de los datos de la compra
        horas_compradas = data.get("horas_compradas")
        precio_por_hora = data.get("precio_por_hora")

        if not horas_compradas or not precio_por_hora:
            return Response({"error": "Se requieren los campos 'horas_compradas' y 'precio_por_hora'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            horas_compradas = int(horas_compradas)
            precio_por_hora = float(precio_por_hora)
        except ValueError:
            return Response({"error": "Los campos 'horas_compradas' y 'precio_por_hora' deben ser numéricos"}, status=status.HTTP_400_BAD_REQUEST)

        if horas_compradas <= 0 or precio_por_hora <= 0:
            return Response({"error": "Las horas y el precio por hora deben ser mayores a cero"}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular el monto total de la compra
        monto_total = horas_compradas * precio_por_hora

        # Crear la compra de horas
        compra = CompraHoras(
            usuario=usuario,
            horas_compradas=horas_compradas,
            precio_por_hora=precio_por_hora,
            monto_total=monto_total
        )
        compra.save()

        return Response({
            "usuario": str(usuario.id),
            "horas_compradas": horas_compradas,
            "precio_por_hora": precio_por_hora,
            "monto_total": monto_total,
            "fecha_compra": compra.fecha_compra.strftime("%Y-%m-%d %H:%M:%S")
        }, status=status.HTTP_201_CREATED)


class ConsultarComprasHorasView(APIView):
    """
    Vista para consultar todas las compras de horas de un usuario.
    """
    def get(self, request, usuario_id):
        """
        Devuelve todas las compras de horas realizadas por un usuario.
        :param usuario_id: ID del usuario
        :return: Response con las compras de horas
        """
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        compras = CompraHoras.objects(usuario=usuario)

        if not compras:
            return Response({"error": "No se encontraron compras de horas para este usuario"}, status=status.HTTP_404_NOT_FOUND)

        # Preparar la respuesta con todas las compras
        compras_data = [{
            "horas_compradas": compra.horas_compradas,
            "precio_por_hora": compra.precio_por_hora,
            "monto_total": compra.monto_total,
            "fecha_compra": compra.fecha_compra.strftime("%Y-%m-%d %H:%M:%S")
        } for compra in compras]

        return Response({"compras": compras_data}, status=status.HTTP_200_OK)
