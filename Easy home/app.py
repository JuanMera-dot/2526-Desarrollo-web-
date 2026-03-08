from flask import Flask, render_template, request, redirect, url_for, session, flash
from inventario import Inventario, Producto, crear_tablas, conectar_db
import sqlite3

# --- 1. IMPORTACIONES ---
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json
import csv
import os
from datetime import datetime

app = Flask(__name__)
# Llave para seguridad y para que funcionen los mensajes flash
app.secret_key = 'uea_tic_secret_2026'

# --- 2. CONFIGURACIÓN DE SQLALCHEMY ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easyhome_orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 3. MODELOS DE DATOS ---

# Tarea de la semana 12
class NuevoServicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

# Expertos con lógica de estrellas
class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profesion = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    proposito = db.Column(db.Text, nullable=False)
    
    solicitudes = db.relationship('Solicitud', backref='experto', lazy=True)
    resenias = db.relationship('Resenia', backref='experto', lazy=True)

    def promedio_estrellas(self):
        if not self.resenias:
            return 0
        total = sum(r.estrellas for r in self.resenias)
        return round(total / len(self.resenias), 1)

# Clientes, Solicitudes y Reseñas
class UsuarioCliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    solicitudes = db.relationship('Solicitud', backref='cliente', lazy=True)
    resenias = db.relationship('Resenia', backref='cliente', lazy=True)

class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario_cliente.id'), nullable=False)
    experto_id = db.Column(db.Integer, db.ForeignKey('profesional.id'), nullable=False)

class Resenia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estrellas = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario_cliente.id'), nullable=False)
    experto_id = db.Column(db.Integer, db.ForeignKey('profesional.id'), nullable=False)

crear_tablas()
inv = Inventario()

# =========================================================
# RUTAS DE VISUALIZACIÓN
# =========================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expertos')
def expertos():
    categorias_db = db.session.query(Profesional.profesion).distinct().all()
    lista_categorias = [c[0] for c in categorias_db]
    todos_los_expertos = Profesional.query.all()
    return render_template('expertos.html', categorias=lista_categorias, expertos=todos_los_expertos)

@app.route('/tienda')
def tienda():
    inv.cargar_desde_db()
    return render_template('tienda.html', productos=inv.productos.values())

@app.route('/suministros')
def suministros():
    inv.cargar_desde_db()
    lista = [p for p in inv.productos.values() if p.categoria == 'Suministros']
    return render_template('suministros.html', suministros=lista)

@app.route('/instrumentos')
def instrumentos():
    inv.cargar_desde_db()
    lista = [p for p in inv.productos.values() if p.categoria == 'Instrumentos']
    return render_template('instrumentos.html', instrumentos=lista)

# =========================================================
# GESTIÓN DE USUARIOS Y SEGURIDAD
# =========================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nuevo_profesional = Profesional(
            nombre=request.form['nombre'], correo=request.form['correo'],
            password=request.form['password'], profesion=request.form['profesion'],
            ubicacion=request.form['ubicacion'], proposito=request.form['proposito']
        )
        try:
            db.session.add(nuevo_profesional)
            db.session.commit()
            flash('✅ Registro de experto exitoso. ¡Bienvenido!', 'success')
            return redirect(url_for('expertos'))
        except IntegrityError:
            db.session.rollback()
            flash('⚠️ El correo ya está registrado.', 'danger')
            return redirect(url_for('registro'))
    return render_template('registro.html')

@app.route('/registro_cliente', methods=['GET', 'POST'])
def registro_cliente():
    if request.method == 'POST':
        nuevo_cliente = UsuarioCliente(
            nombre=request.form['nombre'], correo=request.form['correo'],
            password=request.form['password']
        )
        try:
            db.session.add(nuevo_cliente)
            db.session.commit()
            flash('✅ Cuenta de cliente creada. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('⚠️ Correo ya registrado.', 'danger')
            return redirect(url_for('registro_cliente'))
    return render_template('registro_cliente.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_user = request.form['usuario']
        clave = request.form['password']

        if id_user == 'admin' and clave == '1234':
            session.clear()
            session['es_admin'] = True
            flash('🔑 Acceso concedido como Administrador.', 'info')
            return redirect(url_for('admin'))

        # Intento como Profesional
        experto = Profesional.query.filter_by(correo=id_user).first()
        if experto and experto.password == clave:
            session.clear() 
            session['usuario_id'] = experto.id
            session['nombre_usuario'] = experto.nombre
            session['rol'] = 'experto'
            flash(f'👋 ¡Hola de nuevo, {experto.nombre}!', 'success')
            return redirect(url_for('index'))

        # Intento como Cliente
        cliente = UsuarioCliente.query.filter_by(correo=id_user).first()
        if cliente and cliente.password == clave:
            session.clear()
            session['usuario_id'] = cliente.id
            session['nombre_usuario'] = cliente.nombre
            session['rol'] = 'cliente'
            flash(f'✨ Bienvenido, {cliente.nombre}.', 'success')
            return redirect(url_for('index'))
        
        flash('❌ Datos incorrectos. Verifica tu usuario y contraseña.', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    flash('ℹ️ Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('es_admin'):
        flash('🚫 Acceso restringido. Debes ser administrador.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        nuevo = Producto(None, request.form['nombre'], int(request.form['cantidad']), 
                         float(request.form['precio']), request.form['categoria'])
        inv.agregar_producto(nuevo)
        flash('📦 Producto añadido al inventario con éxito.', 'success')
        return redirect(url_for('admin'))
    inv.cargar_desde_db()
    return render_template('admin.html', productos=inv.productos.values())

@app.route('/contactar/<int:experto_id>', methods=['GET', 'POST'])
def contactar_experto(experto_id):
    if not session.get('usuario_id') or session.get('rol') != 'cliente':
        flash('🔒 Por seguridad, solo los clientes registrados pueden contactar expertos.', 'warning')
        return redirect(url_for('expertos'))
    
    experto = Profesional.query.get_or_404(experto_id)
    
    if session.get('usuario_id') == experto.id and session.get('rol') == 'experto':
        flash('✉️ No puedes enviarte solicitudes a ti mismo.', 'info')
        return redirect(url_for('expertos'))

    if request.method == 'POST':
        nueva_solicitud = Solicitud(mensaje=request.form['mensaje'], cliente_id=session['usuario_id'], experto_id=experto_id)
        db.session.add(nueva_solicitud)
        db.session.commit()
        flash('✅ ¡Solicitud enviada! El experto te responderá pronto.', 'success')
        return redirect(url_for('expertos'))
        
    return render_template('contactar.html', experto=experto)

@app.route('/calificar/<int:experto_id>', methods=['POST'])
def calificar_experto(experto_id):
    """Ruta para que los clientes califiquen a los expertos"""
    if not session.get('usuario_id') or session.get('rol') != 'cliente':
        flash('🔒 Debes ser cliente para calificar.', 'warning')
        return redirect(url_for('expertos'))
    
    nueva_resenia = Resenia(
        estrellas=int(request.form['estrellas']),
        comentario=request.form['comentario'],
        cliente_id=session['usuario_id'],
        experto_id=experto_id
    )
    db.session.add(nueva_resenia)
    db.session.commit()
    flash('⭐ ¡Gracias por tu calificación!', 'success')
    return redirect(url_for('expertos'))

# =========================================================
# TAREA SEMANA 12 (4 FORMATOS)
# =========================================================

@app.route('/registrar_orm', methods=['GET', 'POST'])
def registrar_orm():
    if request.method == 'POST':
        nombre, precio, categoria = request.form['nombre'], float(request.form['precio']), request.form['categoria']
        db.session.add(NuevoServicio(nombre=nombre, precio=precio, categoria=categoria))
        db.session.commit()
        with open('datos.txt', 'a', encoding='utf-8') as f: f.write(f"{nombre},{precio},{categoria}\n")
        lista_j = []
        if os.path.exists('datos.json'):
            with open('datos.json', 'r', encoding='utf-8') as f:
                try: lista_j = json.load(f)
                except: pass
        lista_j.append({"nombre": nombre, "precio": precio, "categoria": categoria})
        with open('datos.json', 'w', encoding='utf-8') as f: json.dump(lista_j, f, indent=4)
        arc = os.path.exists('datos.csv')
        with open('datos.csv', 'a', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            if not arc: w.writerow(['nombre', 'precio', 'categoria'])
            w.writerow([nombre, precio, categoria])
        flash('📝 Datos guardados en los 4 formatos de persistencia.', 'success')
        return redirect(url_for('mostrar_datos'))
    return render_template('registro_orm.html')

@app.route('/datos')
def mostrar_datos():
    s_db = NuevoServicio.query.all()
    d_txt = []
    if os.path.exists('datos.txt'):
        with open('datos.txt', 'r', encoding='utf-8') as f: d_txt = f.readlines()
    d_json = []
    if os.path.exists('datos.json'):
        with open('datos.json', 'r', encoding='utf-8') as f:
            try: d_json = json.load(f)
            except: pass
    d_csv = []
    if os.path.exists('datos.csv'):
        with open('datos.csv', 'r', encoding='utf-8') as f: d_csv = list(csv.reader(f))
    return render_template('datos.html', db=s_db, txt=d_txt, json=d_json, csv=d_csv)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
    