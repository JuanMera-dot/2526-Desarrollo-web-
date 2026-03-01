from flask import Flask, render_template, request, redirect, url_for, session
from inventario import Inventario, Producto, crear_tablas, conectar_db
import sqlite3

app = Flask(__name__)
# Llave para que el sistema de administrador sea seguro
app.secret_key = 'uea_tic_secret_2026'

# Inicializamos la base de datos
crear_tablas()
inv = Inventario()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tienda')
def tienda():
    inv.cargar_desde_db()
    return render_template('tienda.html', productos=inv.productos.values())

@app.route('/suministros')
def suministros():
    inv.cargar_desde_db()
    # Filtramos solo los productos de la categoría Suministros
    lista = [p for p in inv.productos.values() if p.categoria == 'Suministros']
    return render_template('suministros.html', suministros=lista)

@app.route('/instrumentos')
def instrumentos():
    inv.cargar_desde_db()
    # Filtramos solo los productos de la categoría Instrumentos
    lista = [p for p in inv.productos.values() if p.categoria == 'Instrumentos']
    return render_template('instrumentos.html', instrumentos=lista)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO trabajadores (nombre, correo, password, profesion, ubicacion, proposito)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (request.form['nombre'], request.form['correo'], request.form['password'], 
                  request.form['profesion'], request.form['ubicacion'], request.form['proposito']))
            conexion.commit()
            conexion.close()
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            return "<h3>⚠️ El correo ya está registrado.</h3>"
    return render_template('registro.html')

# --- SEGURIDAD BÁSICA PARA EL ADMINISTRADOR ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['password'] == '1234':
            session['es_admin'] = True
            return redirect(url_for('admin'))
        return "<h3>Clave incorrecta</h3>"
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('es_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nuevo = Producto(None, request.form['nombre'], int(request.form['cantidad']), 
                         float(request.form['precio']), request.form['categoria'])
        inv.agregar_producto(nuevo)
        return redirect(url_for('admin'))
    
    inv.cargar_desde_db()
    return render_template('admin.html', productos=inv.productos.values())

@app.route('/logout')
def logout():
    session.pop('es_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
