from flask import Flask

app = Flask(__name__)

# 1. Ruta Principal: Muestra el propósito del negocio
@app.route('/')
def home():
    return """
    <h1>Bienvenido a Easy Home</h1>
    <p>Conectamos profesionales de plomería, electricidad y limpieza con tu hogar.</p>
    <hr>
    <p>Prueba nuestra ruta dinámica agregando a la URL: <b>/servicio/plomeria</b></p>
    """

# 2. Ruta Dinámica: Adaptada a tus servicios
@app.route('/servicio/<nombre_servicio>')
def servicio(nombre_servicio):
    # Mensaje coherente según el ejemplo de la tarea
    return f"<h1>Servicio de {nombre_servicio}</h1><p>Consultando disponibilidad de técnicos para {nombre_servicio} en tu zona. ¡Espera un momento!</p>"

if __name__ == '__main__':
    app.run(debug=True)
    