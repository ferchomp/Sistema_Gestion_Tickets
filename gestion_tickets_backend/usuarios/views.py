from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
from .models import Usuario

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if Usuario.objects.filter(username=username).first():
            return JsonResponse({'error': 'Usuario ya existe'}, status=400)

        if Usuario.objects.filter(email=email).first():
            return JsonResponse({'error': 'El correo electrónico ya está registrado'}, status=400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = Usuario(username=username, password=hashed_password.decode('utf-8'), email=email)
        user.save()
        return JsonResponse({'message': 'Registro exitoso'}, status=201)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = Usuario.objects.filter(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({'message': 'Autenticación satisfactoria'}, status=200)

        return JsonResponse({'error': 'Error en la autenticación'}, status=401)

def home(request):
    return HttpResponse('<h1>Bienvenido al Sistema de Gestión de Tickets</h1>')
