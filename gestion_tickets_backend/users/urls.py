# gestion_tickets_backend/users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),            # Ruta para la página principal
    path('register/', views.register, name='register'),   # Ruta para registro 
    path('login/', views.login_view, name='login'),       # Ruta para inicio de sesión 
 ]