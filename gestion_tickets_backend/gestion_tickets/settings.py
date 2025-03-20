"""
Configuración de Django para el proyecto de Gestión de Tickets.
"""

from pathlib import Path  # 📌 Importamos Path para manejar rutas dentro del proyecto
import mongoengine  # 📌 Importamos mongoengine para la conexión con MongoDB
import os  # 📌 Importamos os para manejar variables de entorno del sistema
from datetime import timedelta  # 📌 Importamos timedelta para manejar la expiración de tokens JWT

# 📌 Definimos la ruta base del proyecto, útil para manejar archivos internos
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚨 Configuración de seguridad
# 📌 Clave secreta usada por Django para firmar datos sensibles (se recomienda cambiarla en producción)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'cambia-esto-en-produccion')

# 📌 Modo de depuración activado o desactivado (se recomienda False en producción)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# 🚨 Lista de hosts permitidos para servir la aplicación (se recomienda especificarlos en producción)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ✅ Configuración de la base de datos MongoDB
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'ticketsdb')  # 📌 Nombre de la base de datos
MONGO_URI = os.getenv('MONGO_URI', f'mongodb://127.0.0.1:27017/{MONGO_DB_NAME}')  # 📌 URI de conexión

# 🔹 Intentamos conectar a MongoDB y mostramos un mensaje en consola
try:
    mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_URI)
    print("✅ Conexión a MongoDB establecida correctamente desde settings.py")
except Exception as e:
    print(f"❌ Error al conectar a MongoDB: {e}")

# 📌 Aplicaciones instaladas en el proyecto Django
INSTALLED_APPS = [
    'django.contrib.admin',  # 📌 Interfaz de administración de Django
    'django.contrib.auth',  # 📌 Manejo de autenticación y permisos de usuarios
    'django.contrib.contenttypes',  # 📌 Manejo de tipos de contenido en la BD
    'django.contrib.sessions',  # 📌 Manejo de sesiones de usuario
    'django.contrib.messages',  # 📌 Sistema de mensajería de Django
    'django.contrib.staticfiles',  # 📌 Archivos estáticos como CSS y JS
    'rest_framework',  # 📌 Django REST Framework para construir APIs
    'rest_framework_simplejwt',  # 📌 Manejo de autenticación con JWT
    'corsheaders',  # 📌 Middleware para manejar CORS (Cross-Origin Resource Sharing)
    'usuarios',  # 📌 Aplicación de usuarios
    'tickets',  # 📌 Aplicación de tickets
    'ayuda_y_soporte',  # 📌 Aplicación de ayuda y soporte
    'reportes',  # 📌 Aplicación de reportes
    'saldo',  # 📌 Aplicación de saldo
    'comprar_horas',  # 📌 Aplicación para la compra de horas
    'departamentos',  # 📌 Aplicación de departamentos
    'django_extensions',  # 📌 Extensiones adicionales para desarrollo
]

# 📌 Configuración de la URL raíz del proyecto
ROOT_URLCONF = 'gestion_tickets.urls'

# ✅ Configuración de Django REST Framework (DRF)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'usuarios.authentication.MongoDBJWTAuthentication',  # 📌 Autenticación personalizada con MongoDB
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 📌 Se requiere autenticación para acceder a las vistas
    ),
}

# ✅ Configuración de autenticación con JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),  # 📌 Expiración del token de acceso en 3 horas
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # 📌 Expiración del token de refresco en 7 días
    'ROTATE_REFRESH_TOKENS': True,  # 📌 Permitir la rotación de tokens de refresco
    'BLACKLIST_AFTER_ROTATION': True,  # 📌 Invalidar el refresh token después de la rotación
    'ALGORITHM': 'HS256',  # 📌 Algoritmo de firma de tokens JWT
    'SIGNING_KEY': SECRET_KEY,  # 📌 Clave secreta para firmar tokens
    'AUTH_HEADER_TYPES': ('Bearer',),  # 📌 Tipo de autenticación usada en los headers HTTP
    'USER_ID_FIELD': 'id',  # 📌 Nombre del campo que representa el usuario en JWT
    'USER_ID_CLAIM': 'user_id',  # 📌 Reclamación que contendrá el ID del usuario en JWT
}

# 📌 Middlewares que actúan sobre las solicitudes HTTP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 📌 Middleware de seguridad de Django
    'django.contrib.sessions.middleware.SessionMiddleware',  # 📌 Manejo de sesiones de usuario
    'corsheaders.middleware.CorsMiddleware',  # 📌 Middleware de CORS para permitir peticiones externas
    'django.middleware.common.CommonMiddleware',  # 📌 Middleware común de Django
    'django.middleware.csrf.CsrfViewMiddleware',  # 📌 Protección contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 📌 Manejo de autenticación de usuarios
    'django.contrib.messages.middleware.MessageMiddleware',  # 📌 Middleware de mensajes de Django
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 📌 Protección contra ataques clickjacking
]

# 📌 Configuración de las plantillas en Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 📌 Motor de plantillas usado
        'DIRS': [],  # 📌 Directorios adicionales de plantillas
        'APP_DIRS': True,  # 📌 Habilita el uso de plantillas dentro de las aplicaciones
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # 📌 Contexto de depuración
                'django.template.context_processors.request',  # 📌 Contexto de la petición HTTP
                'django.contrib.auth.context_processors.auth',  # 📌 Contexto de autenticación
                'django.contrib.messages.context_processors.messages',  # 📌 Contexto de mensajes
            ],
        },
    },
]

# 📌 Configuración del servidor WSGI
WSGI_APPLICATION = 'gestion_tickets.wsgi.application'

# 📌 Configuración de Internacionalización y Zona Horaria
LANGUAGE_CODE = 'es-co'  # 📌 Configuración regional en español de Colombia
TIME_ZONE = 'America/Bogota'  # 📌 Zona horaria configurada para Colombia
USE_I18N = True  # 📌 Habilitar soporte para internacionalización
USE_TZ = True  # 📌 Habilitar uso de zonas horarias

# 📌 Configuración de archivos estáticos
STATIC_URL = '/static/'

# 📌 Configuración de CORS (Cross-Origin Resource Sharing)
CORS_ALLOW_ALL_ORIGINS = True  # 📌 Permitir todas las solicitudes externas (¡Cambiar en producción!)
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]  # 📌 Métodos HTTP permitidos
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type"]  # 📌 Encabezados HTTP permitidos

# 📌 Configuración del Runner de Pruebas
TEST_RUNNER = 'django.test.runner.DiscoverRunner'  # 📌 Manejador de pruebas de Django
