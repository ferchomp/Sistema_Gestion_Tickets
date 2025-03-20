"""
Definición de rutas para la API de usuarios.
"""

from django.urls import path  # 📌 Importamos path para definir rutas manualmente
from rest_framework_simplejwt.views import TokenRefreshView  # 📌 Para refrescar tokens JWT
from .views import UsuarioViewSet, AgentesViewSet, SolicitantesViewSet, register, login_view

# 📌 Definimos las rutas de la API para la gestión de usuarios
urlpatterns = [
    # 📌 Rutas de autenticación
    path("register/", register, name="register"),  # ✅ Registro de usuarios
    path("login/", login_view, name="login"),  # ✅ Inicio de sesión con JWT
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # ✅ Refrescar token JWT

    # 📌 Rutas para la gestión de usuarios
    path("", UsuarioViewSet.as_view({"get": "list"}), name="usuarios-list"),  # ✅ Listar todos los usuarios
    path("actualizar/<str:pk>/", UsuarioViewSet.as_view({"put": "update"}), name="usuarios-update"),  # ✅ Actualizar usuario
    path("delete/<str:pk>/", UsuarioViewSet.as_view({"delete": "destroy"}), name="usuarios-delete"),  # ✅ Eliminar usuario

    # 📌 Rutas para agentes y solicitantes
    path("agentes/", AgentesViewSet.as_view({"get": "list"}), name="usuarios-agentes"),  # ✅ Listar agentes
    path("solicitantes/", SolicitantesViewSet.as_view({"get": "list"}), name="usuarios-solicitantes"),  # ✅ Listar solicitantes
]
