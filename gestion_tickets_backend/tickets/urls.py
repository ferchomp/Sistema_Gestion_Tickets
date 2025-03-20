from django.urls import path
from .views import GetAllTicketsView, CreateTicketView, GetTicketView, UpdateTicketView, DeleteTicketView
from .views import generar_screenshot

urlpatterns = [
    path('', GetAllTicketsView.as_view(), name='get_all_tickets'),
    path('create/', CreateTicketView.as_view(), name='create_ticket'),
    path('<str:id>/', GetTicketView.as_view(), name='get_ticket_by_id'),
    path('<str:id>/update/', UpdateTicketView.as_view(), name='update_ticket'),
    path('<str:id>/delete/', DeleteTicketView.as_view(), name='delete_ticket'),
    path("captura/", generar_screenshot, name="captura"),
]
