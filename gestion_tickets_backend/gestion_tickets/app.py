# gestion_tickets_backend/app.py (puedes crear este archivo)

import mongoengine

# Cadena de conexión a MongoDB
uri = "mongodb://127.0.0.1:27017/ticketsdb"

# Conectar a MongoDB
def connect_to_mongo():
    try:
        mongoengine.connect('ticketsdb', host='127.0.0.1', port=27017)
        print("Conexión a MongoDB establecida con éxito.")
    except mongoengine.ConnectionError as e:
        print(f"Error al conectar a MongoDB: {e}")

# Llamar a la función para realizar la conexión
connect_to_mongo()