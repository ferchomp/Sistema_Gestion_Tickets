from django.contrib import admin
from django.urls import path, include
from usuarios.views import index  # ✅ Importamos la vista de inicio

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', index, name='index'),  # ✅ Ahora la ruta "/" responderá correctamente
    path('usuarios/', include('usuarios.urls')),  # Rutas de la app de usuarios
    path('tickets/', include('tickets.urls')),  # Rutas de la app de tickets
    path('ayuda_y_soporte/', include('ayuda_y_soporte.urls')),  # Rutas de la app de ayuda y soporte
    path('reportes/', include('reportes.urls')),  # Rutas de la app de reportes
    path('saldo/', include('saldo.urls')),  # Rutas de la app de saldo
    path('comprar_horas/', include('comprar_horas.urls')),  # Rutas de la app de comprar horas
    path('departamentos/', include('departamentos.urls')),  # Rutas de la app de departamentos
]
