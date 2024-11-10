# gestion_tickets_backend/users/urls.py

from django.urls import path
from .views import register, login_view, home 

urlpatterns = [
    path('', home, name='home'),               # Ruta para la página principal
    path('register/', register, name='register'),   # Ruta para registro 
    path('login/', login_view, name='login'),       # Ruta para inicio de sesión 
]