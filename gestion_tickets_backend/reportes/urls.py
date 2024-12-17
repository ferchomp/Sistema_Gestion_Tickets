# urls.py
from django.urls import path
from .views import ReporteTicketsView, ExportarReporteTicketsView

urlpatterns = [
    path('reporte-tickets/', ReporteTicketsView.as_view(), name='reporte-tickets'),
    path('exportar-reporte-tickets/', ExportarReporteTicketsView.as_view(), name='exportar-reporte-tickets'),
]