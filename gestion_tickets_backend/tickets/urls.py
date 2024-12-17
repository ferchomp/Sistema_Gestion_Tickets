from django.urls import path
from .views import (
    GetAllTicketsView,
    CreateTicketView,
    GetTicketView,
    UpdateTicketView,
    DeleteTicketView
)

urlpatterns = [
    path('', GetAllTicketsView.as_view(), name='get_all_tickets'),  # Listar todos los tickets
    path('create/', CreateTicketView.as_view(), name='create_ticket'),  # Crear un nuevo ticket
    path('<str:id>/', GetTicketView.as_view(), name='get_ticket'),  # Obtener un ticket específico
    path('<str:id>/update/', UpdateTicketView.as_view(), name='update_ticket'),  # Actualizar un ticket
    path('<str:id>/delete/', DeleteTicketView.as_view(), name='delete_ticket'),  # Eliminar un ticket
]
