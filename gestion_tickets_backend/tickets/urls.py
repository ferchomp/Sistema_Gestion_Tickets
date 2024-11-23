from django.urls import path
from .views import create_ticket, get_all_tickets, get_ticket, update_ticket, delete_ticket

urlpatterns = [
    path('create/', create_ticket, name='create_ticket'),
    path('', get_all_tickets, name='get_all_tickets'),
    path('<str:ticket_id>/', get_ticket, name='get_ticket'),
    path('update/<str:ticket_id>/', update_ticket, name='update_ticket'),
    path('delete/<str:ticket_id>/', delete_ticket, name='delete_ticket'),
]
