from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Renderizamos la página de inicio
    return render_template('index.html')

@app.route('/about')
def about():
    # Renderizamos la página de acerca de
    return render_template('about.html')

# Puedes agregar más rutas para tu proyecto (servicios, clientes, etc.)
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

if __name__ == '__main__':
    app.run(debug=True)

    


