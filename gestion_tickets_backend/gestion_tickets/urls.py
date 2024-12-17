from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('usuarios/', include('usuarios.urls')),  # Rutas de la app de usuarios
    path('tickets/', include('tickets.urls')),    # Rutas de la app de tickets
    path('ayuda_y_soporte/', include('ayuda_y_soporte.urls')),  # Rutas de la app de ayuda y soporte
    path('reportes/', include('reportes.urls')),  # Rutas de la app de reportes
    path('', include('usuarios.urls')),  # Ruta principal para la página de bienvenida (home)
    path('saldo/', include('saldo.urls')),  # Rutas de la app de saldo
    path('comprar_horas/', include('comprar_horas.urls')), # Rutas de la app de comprar horas
]
