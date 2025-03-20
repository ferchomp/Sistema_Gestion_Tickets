from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Departamento

@method_decorator(csrf_exempt, name='dispatch')  # Desactiva CSRF para esta vista
class ListaDepartamentos(View):
    """Vista para obtener y crear departamentos"""

    def get(self, request):
        """Obtiene todos los departamentos disponibles"""
        departamentos = Departamento.objects.all().only("id", "nombre")
        data = [{"id": str(dep.id), "nombre": dep.nombre} for dep in departamentos]
        return JsonResponse(data, safe=False, status=200)

    def post(self, request):
        """Crea un nuevo departamento si no existe"""
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")

            if not nombre:
                return JsonResponse({"error": "El campo 'nombre' es obligatorio"}, status=400)

            if Departamento.objects(nombre=nombre).first():
                return JsonResponse({"error": "El departamento ya existe"}, status=400)

            nuevo_departamento = Departamento(nombre=nombre)
            nuevo_departamento.save()

            return JsonResponse({"message": "Departamento creado con éxito", "id": str(nuevo_departamento.id)}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
