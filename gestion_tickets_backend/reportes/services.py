from tickets.models import Ticket  # Importar el modelo Ticket desde la app tickets
from io import BytesIO
from openpyxl import Workbook

def generar_reporte_tickets(filtros):
    """
    Filtra y genera un reporte basado en los datos de tickets.
    """
    tickets = Ticket.objects()  # Consulta a la colección Ticket en MongoDB

    # Aplicar los filtros según lo recibido
    if 'estado_ticket' in filtros:
        tickets = tickets.filter(estado_ticket=filtros['estado_ticket'])
    if 'asignado' in filtros:
        tickets = tickets.filter(asignado=filtros['asignado'])
    if 'solicitante' in filtros:
        tickets = tickets.filter(solicitante=filtros['solicitante'])

    # Formatear los datos para el reporte
    datos = [
        {
            "ticket_id": str(ticket.id),
            "estado_ticket": ticket.estado_ticket,
            "asignado": ticket.asignado
        }
        for ticket in tickets
    ]

    return datos

def generar_reporte_tickets_excel(filtros):
    """
    Genera un archivo Excel con los datos de los tickets filtrados.
    """
    datos = generar_reporte_tickets(filtros)

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de Tickets"
    ws.append(["ID", "Estado", "Asignado"])  # Encabezados del Excel

    for ticket in datos:
        ws.append([ticket["ticket_id"], ticket["estado_ticket"], ticket["asignado"]])

    archivo_memoria = BytesIO()
    wb.save(archivo_memoria)
    archivo_memoria.seek(0)

    return archivo_memoria
