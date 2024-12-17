# urls.py de la aplicación 'comprar_horas'
from django.urls import path
from .views import ComprarHorasView, ConsultarComprasHorasView

urlpatterns = [
    path('comprar/<str:usuario_id>/', ComprarHorasView.as_view(), name='comprar_horas'),
    path('consultar/<str:usuario_id>/', ConsultarComprasHorasView.as_view(), name='consultar_compras_horas'),
]
