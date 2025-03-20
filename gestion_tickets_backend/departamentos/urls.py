from django.urls import path
from .views import ListaDepartamentos

urlpatterns = [
    path('', ListaDepartamentos.as_view(), name='departamentos'),
]
