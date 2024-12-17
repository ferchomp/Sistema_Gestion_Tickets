# views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import generar_reporte_tickets, generar_reporte_tickets_excel  # Asegúrate de que estos servicios existan correctamente

class ReporteTicketsView(APIView):
    """
    Vista para generar el reporte de tickets en formato JSON.
    """
    def get(self, request):
        try:
            filtros = self._extraer_filtros(request)
            reporte = generar_reporte_tickets(filtros)  # Método en services.py para obtener los datos

            if not reporte:
                return Response(
                    {"mensaje": "No se encontraron tickets con los filtros aplicados."},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({"tickets": reporte}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": f"Error de validación: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _extraer_filtros(self, request):
        """
        Extrae los filtros desde los parámetros de consulta.
        """
        filtros = {}
        estado = request.query_params.get('estado')
        asignado = request.query_params.get('asignado')
        solicitante = request.query_params.get('solicitante')

        # Solo agregar filtros si tienen valor
        if estado:
            filtros['estado_ticket'] = estado
        if asignado:
            filtros['asignado'] = asignado
        if solicitante:
            filtros['solicitante'] = solicitante

        return filtros

class ExportarReporteTicketsView(APIView):
    """
    Vista para exportar el reporte de tickets en formato Excel.
    """
    def get(self, request):
        try:
            filtros = self._extraer_filtros(request)
            archivo_memoria = generar_reporte_tickets_excel(filtros)  # Método en services.py para crear el archivo

            if not archivo_memoria:
                return Response(
                    {"mensaje": "No se encontraron tickets con los filtros aplicados."},
                    status=status.HTTP_404_NOT_FOUND
                )

            response = HttpResponse(
                archivo_memoria,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="reporte_tickets.xlsx"'
            return response
        except ValueError as e:
            return Response({"error": f"Error de validación: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _extraer_filtros(self, request):
        """
        Extrae los filtros desde los parámetros de consulta.
        """
        filtros = {}
        estado = request.query_params.get('estado')
        asignado = request.query_params.get('asignado')
        solicitante = request.query_params.get('solicitante')

        # Solo agregar filtros si tienen valor
        if estado:
            filtros['estado_ticket'] = estado
        if asignado:
            filtros['asignado'] = asignado
        if solicitante:
            filtros['solicitante'] = solicitante

        return filtros