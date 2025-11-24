import ssl
import mysql.connector
from flask import Flask
from pyngrok import ngrok

# Importar tus rutas
from src.Routes.route import modelRoute

# Configuración SSL para evitar errores de certificado locales
ssl._create_default_https_context = ssl._create_unverified_context

# Configurar token de Ngrok (Asegúrate de que este token sea válido)
ngrok.set_auth_token('35Rw5XJhEjlSdbyQf3aIuzIP13b_bHGZBYah2RPvQq7GCrFc')

app = Flask(__name__)

# --- CLAVE SECRETA PARA SESIONES (LOGIN) ---
# Esto es obligatorio para usar sessions en Flask
app.secret_key = 'clave_super_secreta_para_sesion_uni'

# Inicializar rutas
modelRoute(app)

if __name__ == "__main__":
    # Iniciar túnel Ngrok en el puerto 5000
    public_url = ngrok.connect(5000)
    public_url_str = str(public_url)
    print('URL pública de Ngrok:', public_url_str)
    
    # Iniciar aplicación Flask
    app.run()