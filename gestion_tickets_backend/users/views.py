# gestion_tickets_backend/users/views.py

from django.http import JsonResponse, HttpResponse 
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.objects(username=username).first():
            return JsonResponse({'error': 'Usuario ya existe'}, status=400)

        user = User(username=username, password=password, email=email)
        user.save()
        return JsonResponse({'message': 'Registro exitoso'}, status=201)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects(username=username, password=password).first()

        if user:
            return JsonResponse({'message': 'Autenticación satisfactoria'}, status=200)
        return JsonResponse({'error': 'Error en la autenticación'}, status=401)

def home(request):
    return HttpResponse('<h1>Bienvenido al Sistema de Gestión de Tickets</h1>')
