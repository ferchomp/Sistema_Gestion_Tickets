from django.shortcuts import render
import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mongoengine.errors import ValidationError
from .models import Ticket
from pytz import timezone

@csrf_exempt
def create_ticket(request):
    """Crea un nuevo ticket."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Obtener las fechas de 'data' y convertirlas a zona horaria UTC
            fecha_creacion_str = data['fecha_creacion']
            fecha_resolucion_str = data.get('fecha_resolucion')

            # Convertir 'fecha_creacion' a datetime y luego a UTC
            fecha_creacion = datetime.fromisoformat(fecha_creacion_str).astimezone(timezone('UTC'))

            # Si 'fecha_resolucion' está presente, convertirlo también
            fecha_resolucion = None
            if fecha_resolucion_str:
                fecha_resolucion = datetime.fromisoformat(fecha_resolucion_str).astimezone(timezone('UTC'))

            # Crear el ticket
            ticket = Ticket(
                asignado=data['asignado'],
                solicitante=data['solicitante'],
                departamento=data['departamento'],
                fecha_creacion=fecha_creacion,
                asunto=data['asunto'],
                descripcion=data['descripcion'],
                tipo_ticket=data['tipo_ticket'],
                estado_ticket=data['estado_ticket'],
                prioridad=data['prioridad'],
                fecha_resolucion=fecha_resolucion,
                adjunto=data.get('adjunto')
            )

            ticket.save()
            return JsonResponse({'message': 'Ticket creado exitosamente', 'id': str(ticket.id)}, status=201)
        except ValidationError as ve:
            return JsonResponse({'error': f'Error de validación: {str(ve)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def get_all_tickets(request):
    """Obtiene una lista de todos los tickets."""
    if request.method == 'GET':
        tickets = Ticket.objects()
        tickets_list = [
            {
                "id": str(ticket.id),
                "asignado": ticket.asignado,
                "solicitante": ticket.solicitante,
                "departamento": ticket.departamento,
                "fecha_creacion": str(ticket.fecha_creacion),
                "asunto": ticket.asunto,
                "descripcion": ticket.descripcion,
                "tipo_ticket": ticket.tipo_ticket,
                "estado_ticket": ticket.estado_ticket,
                "prioridad": ticket.prioridad,
                "fecha_resolucion": str(ticket.fecha_resolucion) if ticket.fecha_resolucion else None,
            }
            for ticket in tickets
        ]
        return JsonResponse(tickets_list, safe=False, status=200)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def get_ticket(request, ticket_id):
    """Obtiene los detalles de un ticket específico."""
    if request.method == 'GET':
        ticket = Ticket.objects(id=ticket_id).first()
        if ticket:
            ticket_data = {
                "id": str(ticket.id),
                "asignado": ticket.asignado,
                "solicitante": ticket.solicitante,
                "departamento": ticket.departamento,
                "fecha_creacion": str(ticket.fecha_creacion),
                "asunto": ticket.asunto,
                "descripcion": ticket.descripcion,
                "tipo_ticket": ticket.tipo_ticket,
                "estado_ticket": ticket.estado_ticket,
                "prioridad": ticket.prioridad,
                "fecha_resolucion": str(ticket.fecha_resolucion) if ticket.fecha_resolucion else None,
            }
            return JsonResponse(ticket_data, status=200)
        return JsonResponse({'error': 'Ticket no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def update_ticket(request, ticket_id):
    """Actualiza los datos de un ticket."""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            ticket = Ticket.objects(id=ticket_id).first()
            if ticket:
                if 'fecha_creacion' in data:
                    ticket.fecha_creacion = datetime.fromisoformat(data['fecha_creacion']).astimezone(timezone('UTC'))
                ticket.asignado = data.get('asignado', ticket.asignado)
                ticket.solicitante = data.get('solicitante', ticket.solicitante)
                ticket.departamento = data.get('departamento', ticket.departamento)
                ticket.asunto = data.get('asunto', ticket.asunto)
                ticket.descripcion = data.get('descripcion', ticket.descripcion)
                ticket.tipo_ticket = data.get('tipo_ticket', ticket.tipo_ticket)
                ticket.estado_ticket = data.get('estado_ticket', ticket.estado_ticket)
                ticket.prioridad = data.get('prioridad', ticket.prioridad)

                if 'fecha_resolucion' in data:
                    ticket.fecha_resolucion = datetime.fromisoformat(data['fecha_resolucion']).astimezone(timezone('UTC'))
                
                ticket.save()
                return JsonResponse({'message': 'Ticket actualizado exitosamente'}, status=200)
            return JsonResponse({'error': 'Ticket no encontrado'}, status=404)
        except ValidationError as ve:
            return JsonResponse({'error': f'Error de validación: {str(ve)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def delete_ticket(request, ticket_id):
    """Elimina un ticket."""
    if request.method == 'DELETE':
        try:
            ticket = Ticket.objects(id=ticket_id).first()
            if ticket:
                ticket.delete()
                return JsonResponse({'message': 'Ticket eliminado exitosamente'}, status=200)
            return JsonResponse({'error': 'Ticket no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
