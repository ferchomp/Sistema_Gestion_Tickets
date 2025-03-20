from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer
from mongoengine.errors import DoesNotExist, ValidationError
from datetime import datetime
import traceback
from mongoengine.errors import DoesNotExist, ValidationError
from usuarios.models import Usuario
from django.http import JsonResponse
from tickets.utils.screenshot import capture_screenshot  # Asegúrate de que la importación es correcta

def generar_screenshot(request):
    print(f"📥 Método de la solicitud: {request.method}")  # Depuración
    
    if request.method != "GET":
        print("❌ Error: Método no permitido")  
        return JsonResponse({"error": "Método no permitido"}, status=400)

    try:
        output_path = "gestion_tickets_backend/static/ticket_screenshot.png"
        print(f"📸 Capturando pantalla en: {output_path}")

        capture_screenshot("http://localhost:5173/tickets", output_path)

        print(f"✅ Captura guardada correctamente en {output_path}")
        return JsonResponse({
            "message": "Captura de pantalla creada con éxito",
            "path": "/static/ticket_screenshot.png"
        })

    except Exception as e:
        print(f"❌ Error en captura: {e}")  # Imprime el error
        return JsonResponse({"error": str(e)}, status=500)

class GetAllTicketsView(APIView):
    """Obtiene todos los tickets almacenados en MongoDB."""
    def get(self, request):
        try:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("🚨 ERROR:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTicketView(APIView):
    """Obtiene un solo ticket por su ID."""
    def get(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoesNotExist:
            return Response({"error": "Ticket no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({"error": "ID de ticket no válido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("🚨 ERROR:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTicketView(APIView):
    """Crea un nuevo ticket en MongoDB con asignación automática de usuario."""
    def post(self, request):
        try:
            data = request.data.copy()
            print("📥 Datos recibidos en la solicitud:", data)

            # 🔹 Convertir fechas si son string
            for field in ["fecha_creacion", "fecha_resolucion"]:
                if field in data and isinstance(data[field], str):
                    try:
                        formatos_validos = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
                        for formato in formatos_validos:
                            try:
                                data[field] = datetime.strptime(data[field], formato)
                                break
                            except ValueError:
                                continue
                        else:
                            return Response({"error": f"Formato de {field} inválido. Usa: YYYY-MM-DDTHH:MM:SS.sssZ, YYYY-MM-DD HH:MM:SS o YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
                    except ValueError:
                        return Response({"error": f"Formato de {field} inválido."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TicketSerializer(data=data)
            if serializer.is_valid():
                ticket = serializer.save()

                # 🔹 Buscar un usuario disponible (menos tickets abiertos)
                usuario_disponible = Usuario.objects.filter(rol="soporte").order_by('tickets_abiertos').first()
                if usuario_disponible:
                    ticket.asignado = usuario_disponible
                    ticket.save()

                return Response({"message": "Ticket creado con éxito", "id": str(ticket.id)}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("🚨 ERROR:", str(e))
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateTicketView(APIView):
    """Actualiza un ticket en MongoDB por su ID."""
    
    def put(self, request, id):
        try:
            # 🔹 Buscar el ticket en la base de datos
            ticket = Ticket.objects.get(id=id)
            data = request.data.copy()
            print("📥 Datos recibidos:", data)

            # 🔹 Validar que haya al menos un parámetro válido en la solicitud
            campos_validos = ["estado_ticket", "fecha_resolucion"]
            datos_actualizar = {k: v for k, v in data.items() if k in campos_validos}
            
            if not datos_actualizar:
                return Response({"error": "No hay datos válidos para actualizar"}, status=status.HTTP_400_BAD_REQUEST)

            # 🔹 Validar el formato de fecha_resolucion (si se envía)
            if "fecha_resolucion" in datos_actualizar:
                try:
                    datos_actualizar["fecha_resolucion"] = datetime.strptime(datos_actualizar["fecha_resolucion"], "%Y-%m-%d")
                except ValueError:
                    return Response({"error": "Formato de fecha_resolucion inválido. Usa YYYY-MM-DD"}, 
                                    status=status.HTTP_400_BAD_REQUEST)

            # 🔹 Aplicar los cambios y guardar
            ticket.modify(**datos_actualizar)
            
            # 🔹 Recargar el objeto actualizado de la base de datos
            ticket_actualizado = Ticket.objects.get(id=id)

            # 🔹 Serializar y devolver el ticket actualizado
            serializer = TicketSerializer(ticket_actualizado)

            return Response({
                "message": "Ticket actualizado con éxito",
                "ticket": serializer.data  # 🔹 Ahora devuelve los datos actualizados correctamente
            }, status=status.HTTP_200_OK)

        except DoesNotExist:
            return Response({"error": "Ticket no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({"error": "ID no válido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("🚨 ERROR en la actualización:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteTicketView(APIView):
    """Elimina un ticket de MongoDB por su ID."""
    def delete(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
            ticket.delete()
            return Response({"message": "Ticket eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except DoesNotExist:
            return Response({"error": "Ticket no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({"error": "ID no válido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

