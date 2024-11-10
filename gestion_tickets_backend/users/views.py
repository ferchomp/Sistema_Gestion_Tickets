# gestion_tickets_backend/users/views.py

from django.http import JsonResponse, HttpResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Desactivar CSRF para simplificar (no recomendado en producción)
def register(request):
    """Registra un nuevo usuario."""
    if request.method == 'POST':
        data = json.loads(request.body)  # Cargar datos JSON del cuerpo de la solicitud
        username = data.get('username')   # Obtener nombre de usuario del JSON
        password = data.get('password')     # Obtener contraseña del JSON
        email = data.get('email')           # Obtener email del JSON

        if User.objects(username=username).first():  # Verificar si el usuario ya existe
            return JsonResponse({'error': 'Usuario ya existe'}, status=400)

        user = User(username=username, password=password, email=email)  # Crear nuevo usuario
        user.save()  # Guardar usuario en la base de datos
        return JsonResponse({'message': 'Registro exitoso'}, status=201)  # Respuesta exitosa

@csrf_exempt  
def login_view(request):
    """Inicia sesión con un usuario existente."""
    if request.method == 'POST':
        data = json.loads(request.body)  # Cargar datos JSON del cuerpo de la solicitud
        username = data.get('username')   # Obtener nombre de usuario del JSON
        password = data.get('password')     # Obtener contraseña del JSON

        user = User.objects(username=username, password=password).first()  # Autenticación del usuario
        
        if user:
            return JsonResponse({'message': 'Autenticación satisfactoria'}, status=200)  # Autenticación exitosa
        else:
            return JsonResponse({'error': 'Error en la autenticación'}, status=401)  # Error en la autenticación

def home(request):
    """Página principal."""
    return HttpResponse('<center><h1 style="font-size: 48px;">Bienvenido al Sistema de Gestión de Tickets</h1></center>')