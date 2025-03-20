"""
Autenticación personalizada con JWT para MongoDB.
"""

from rest_framework.authentication import BaseAuthentication  # 📌 Base para autenticación personalizada
from rest_framework.exceptions import AuthenticationFailed  # 📌 Excepción en caso de error en autenticación
from rest_framework_simplejwt.tokens import AccessToken  # 📌 Manejo de tokens JWT
from rest_framework_simplejwt.exceptions import TokenError  # 📌 Manejo de errores en JWT
from .models import Usuario  # 📌 Importamos el modelo de Usuario
from bson import ObjectId  # 📌 Importamos ObjectId para manejar IDs en MongoDB

class MongoDBJWTAuthentication(BaseAuthentication):
    """
    Clase de autenticación personalizada para trabajar con JWT en MongoDB.
    """

    def authenticate(self, request):
        # 📌 Obtenemos el token desde la cabecera Authorization
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No se proporciona token

        token_str = auth_header.split(" ")[1]  # Extraemos el token

        try:
            # 📌 Decodificamos el token para obtener el payload
            access_token = AccessToken(token_str)
            user_id = access_token["user_id"]  # Extraemos el ID del usuario

            # 📌 Buscamos al usuario en MongoDB
            usuario = Usuario.objects(id=user_id).first()

            if not usuario:
                raise AuthenticationFailed("Usuario no encontrado")

            return usuario, None  # Devuelve el usuario autenticado

        except Exception:
            raise AuthenticationFailed("Token inválido o expirado")