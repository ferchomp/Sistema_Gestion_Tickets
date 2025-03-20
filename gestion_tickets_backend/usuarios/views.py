"""
Vistas para la gestión de usuarios en la API.
"""

from django.http import JsonResponse  # 📌 Para enviar respuestas JSON
from django.views.decorators.csrf import csrf_exempt  # 📌 Para deshabilitar CSRF en vistas específicas
import json  # 📌 Para manejar datos en formato JSON
import bcrypt  # 📌 Para encriptar contraseñas
from rest_framework import viewsets, status  # 📌 Para crear API con Django REST Framework
from rest_framework.response import Response  # 📌 Para estructurar respuestas API
from rest_framework.permissions import IsAuthenticated  # 📌 Para restringir accesos a endpoints
from rest_framework_simplejwt.tokens import RefreshToken  # 📌 Para manejar autenticación JWT
from .models import Usuario  # 📌 Importamos el modelo de usuarios en MongoDB


# ✅ Vista de prueba para verificar que el servidor está funcionando
def index(request):
    """
    Retorna un mensaje de bienvenida al acceder a la ruta raíz del servidor.
    """
    return JsonResponse({"message": "Bienvenido al Sistema de Gestión de Tickets"}, safe=False)

# ✅ Registro de usuarios en MongoDB
@csrf_exempt
def register(request):
    """
    Registra un nuevo usuario en la base de datos.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            rol = data.get('rol', 'solicitante').lower()

            if not username or not email or not password:
                return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

            if Usuario.objects(username=username).first():
                return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)
            if Usuario.objects(email=email).first():
                return JsonResponse({'error': 'El correo ya está registrado'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            usuario = Usuario(username=username, email=email, password=hashed_password, rol=rol)
            usuario.save()

            return JsonResponse({'message': 'Usuario registrado con éxito', 'id': str(usuario.id)}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

# ✅ Inicio de sesión con JWT
@csrf_exempt
def login_view(request):
    """
    Inicia sesión y genera un token JWT para el usuario autenticado.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido. Usa POST."}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        usuario = Usuario.objects(username=username).first()

        if not usuario or not bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
            return JsonResponse({"error": "Credenciales inválidas"}, status=401)

        refresh = RefreshToken.for_user(usuario)

        return JsonResponse({
            "message": "Inicio de sesión exitoso",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": str(usuario.id),
                "username": usuario.username,
                "email": usuario.email,
                "rol": usuario.rol
            }
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)


# ✅ Vista para listar y modificar usuarios
class UsuarioViewSet(viewsets.ViewSet):
    """
    API para gestionar usuarios.
    """
    permission_classes = [IsAuthenticated]  # 📌 Se requiere autenticación

    def list(self, request):
        """
        Retorna un listado de todos los usuarios.
        """
        usuarios = Usuario.objects.only("id", "username", "email", "rol")
        return Response([
            {"id": str(u.id), "username": u.username, "email": u.email, "rol": u.rol}
            for u in usuarios
        ], status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Actualiza los datos de un usuario específico por su ID.
        """
        try:
            usuario = Usuario.objects(id=pk).first()
            if not usuario:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            data = json.loads(request.body)

            if "email" in data:
                usuario.email = data["email"]
            if "rol" in data:
                usuario.rol = data["rol"]

            usuario.save()

            return Response({"message": "Usuario actualizado con éxito", "id": str(usuario.id)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """
        Elimina un usuario por su ID.
        """
        try:
            usuario = Usuario.objects(id=pk).first()
            if not usuario:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            usuario.delete()

            return Response({"message": "Usuario eliminado con éxito"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ ViewSet para listar agentes
class AgentesViewSet(viewsets.ViewSet):
    """
    API para listar los agentes registrados en el sistema.
    """
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación

    def list(self, request):
        """
        Retorna una lista de todos los usuarios con rol 'agente'.
        """
        agentes = Usuario.objects.filter(rol="agente").only("id", "username", "email", "rol")
        return Response(
            [{"id": str(u.id), "username": u.username, "email": u.email, "rol": u.rol} for u in agentes],
            status=status.HTTP_200_OK
        )


# ✅ ViewSet para listar solicitantes
class SolicitantesViewSet(viewsets.ViewSet):
    """
    API para listar los solicitantes registrados en el sistema.
    """
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación

    def list(self, request):
        """
        Retorna una lista de todos los usuarios con rol 'solicitante'.
        """
        solicitantes = Usuario.objects.filter(rol="solicitante").only("id", "username", "email", "rol")
        return Response(
            [{"id": str(u.id), "username": u.username, "email": u.email, "rol": u.rol} for u in solicitantes],
            status=status.HTTP_200_OK
        )
