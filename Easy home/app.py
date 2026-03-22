from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify # <--- Se agregó jsonify
from inventario import Inventario, Producto, crear_tablas, conectar_db
import sqlite3

# --- 1. IMPORTACIONES ---
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json
import csv
import os
from datetime import datetime

# --- NUEVA IMPORTACIÓN PARA MYSQL ---
from conexion.conexion import obtener_conexion

app = Flask(__name__)
# Llave para seguridad y para que funcionen los mensajes flash
app.secret_key = 'uea_tic_secret_2026'

# --- 2. CONFIGURACIÓN DE SQLALCHEMY ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easyhome_orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 3. MODELOS DE DATOS ---

# Tarea semana 12
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
    
    # --- NUEVOS CAMPOS PARA EL MAPA ---
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    
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
        nombre_form = request.form['nombre']
        correo_form = request.form['correo']
        password_form = request.form['password']

        # 1. GUARDADO EN MYSQL (Tarea Semana 13)
        conexion_mysql = obtener_conexion()
        if conexion_mysql:
            try:
                cursor = conexion_mysql.cursor()
                sql = "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)"
                valores = (nombre_form, correo_form, password_form)
                cursor.execute(sql, valores)
                conexion_mysql.commit()
            except Exception as e:
                print(f"Error guardando en MySQL: {e}")
            finally:
                cursor.close()
                conexion_mysql.close()

        # 2. GUARDADO EN SQLITE
        nuevo_cliente = UsuarioCliente(nombre=nombre_form, correo=correo_form, password=password_form)
        try:
            db.session.add(nuevo_cliente)
            db.session.commit()
            flash('✅ Cuenta de cliente creada.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('⚠️ Correo ya registrado.', 'danger')
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

        experto = Profesional.query.filter_by(correo=id_user).first()
        if experto and experto.password == clave:
            session.clear() 
            session['usuario_id'] = experto.id
            session['nombre_usuario'] = experto.nombre
            session['rol'] = 'experto'
            return redirect(url_for('index'))

        cliente = UsuarioCliente.query.filter_by(correo=id_user).first()
        if cliente and cliente.password == clave:
            session.clear()
            session['usuario_id'] = cliente.id
            session['nombre_usuario'] = cliente.nombre
            session['rol'] = 'cliente'
            return redirect(url_for('index'))
        
        flash('❌ Datos incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    flash('ℹ️ Sesión cerrada.', 'info')
    return redirect(url_for('index'))

# --- RUTA PARA EL LOGIN DE COLABORADORES ---
@app.route('/portal-colaboradores', methods=['GET', 'POST'])
def portal_colaboradores():
    if request.method == 'POST':
        correo_login = request.form.get('correo')
        password_login = request.form.get('password')
        
        experto = Profesional.query.filter_by(correo=correo_login).first()
        
        if experto and experto.password == password_login:
            session.clear() 
            session['usuario_id'] = experto.id
            session['nombre_usuario'] = experto.nombre
            session['rol'] = 'experto'
            flash(f'👋 Bienvenido de nuevo, {experto.nombre}.', 'success')
            
            # ¡AQUÍ ESTÁ EL CAMBIO! Ahora te envía al panel exclusivo
            return redirect(url_for('dashboard_colaborador')) 
        else:
            flash('❌ Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('portal_colaboradores'))
            
    return render_template('login_colaborador.html')

# --- NUEVA RUTA: EL PANEL DE CONTROL (DASHBOARD) ---
@app.route('/dashboard-colaborador')
def dashboard_colaborador():
    # Verificamos que sea un experto logueado, si no, lo mandamos al login
    if not session.get('usuario_id') or session.get('rol') != 'experto':
        return redirect(url_for('portal_colaboradores'))
    
    # Traemos todos los datos del experto desde la base de datos
    experto = Profesional.query.get(session['usuario_id'])
    
    # Renderizamos la nueva plantilla oscura y le pasamos los datos
    return render_template('dashboard_colaborador.html', experto=experto)


# =========================================================
# ADMINISTRACIÓN Y SINCRONIZACIÓN (SQLITE + MYSQL)
# =========================================================

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('es_admin'):
        flash('🚫 Acceso restringido.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        categoria = request.form['categoria']

        # Guardar en MySQL
        conexion_mysql = obtener_conexion()
        if conexion_mysql:
            try:
                cursor = conexion_mysql.cursor()
                sql = "INSERT INTO productos (nombre, precio, cantidad, categoria) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre, precio, cantidad, categoria))
                conexion_mysql.commit()
            finally:
                cursor.close(); conexion_mysql.close()

        # Guardar en SQLite
        nuevo = Producto(None, nombre, cantidad, precio, categoria)
        inv.agregar_producto(nuevo)
        flash('📦 Producto añadido con éxito.', 'success')
        return redirect(url_for('admin'))

    inv.cargar_desde_db()
    return render_template('admin.html', productos=inv.productos.values())

# --- RUTA PARA BORRAR PRODUCTO DESDE PANEL ADMIN ---
@app.route('/borrar_producto_admin/<int:id>')
def borrar_producto_admin(id):
    if not session.get('es_admin'):
        return redirect(url_for('login'))

    # 1. Borrar de SQLite y obtener el nombre del producto
    nombre_borrado = inv.eliminar_producto(id)

    # 2. Si el producto existía, lo borramos de MySQL por su nombre
    if nombre_borrado:
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM productos WHERE nombre = %s", (nombre_borrado,))
                conexion.commit()
                flash(f'🗑️ "{nombre_borrado}" eliminado de todo el sistema.', 'warning')
            except Exception as e:
                print(f"Error borrando en MySQL: {e}")
            finally:
                cursor.close(); conexion.close()
    
    return redirect(url_for('admin'))

@app.route('/contactar/<int:experto_id>', methods=['GET', 'POST'])
def contactar_experto(experto_id):
    if not session.get('usuario_id') or session.get('rol') != 'cliente':
        flash('🔒 Acceso restringido.', 'warning')
        return redirect(url_for('expertos'))
    experto = Profesional.query.get_or_404(experto_id)
    if request.method == 'POST':
        nueva_solicitud = Solicitud(mensaje=request.form['mensaje'], cliente_id=session['usuario_id'], experto_id=experto_id)
        db.session.add(nueva_solicitud)
        db.session.commit()
        flash('✅ Solicitud enviada.', 'success')
        return redirect(url_for('expertos'))
    return render_template('contactar.html', experto=experto)

@app.route('/calificar/<int:experto_id>', methods=['POST'])
def calificar_experto(experto_id):
    if not session.get('usuario_id') or session.get('rol') != 'cliente':
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
        # Guardar en TXT, JSON, CSV...
        with open('datos.txt', 'a', encoding='utf-8') as f: f.write(f"{nombre},{precio},{categoria}\n")
        flash('📝 Datos guardados en los 4 formatos.', 'success')
        return redirect(url_for('mostrar_datos'))
    return render_template('registro_orm.html')

@app.route('/datos')
def mostrar_datos():
    s_db = NuevoServicio.query.all()
    d_txt = []
    if os.path.exists('datos.txt'):
        with open('datos.txt', 'r', encoding='utf-8') as f: d_txt = f.readlines()
    return render_template('datos.html', db=s_db, txt=d_txt)

# =========================================================
# GESTIÓN OCULTA MYSQL (CRUD SEMANA 13)
# =========================================================

@app.route('/admin_mysql')
def admin_mysql():
    conexion = obtener_conexion()
    usuarios_db = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            usuarios_db = cursor.fetchall()
        finally:
            cursor.close(); conexion.close()
    return render_template('admin_mysql.html', usuarios=usuarios_db)

@app.route('/eliminar_mysql/<int:id>')
def eliminar_mysql(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
            conexion.commit()
        finally:
            cursor.close(); conexion.close()
    return redirect(url_for('admin_mysql'))

@app.route('/editar_mysql/<int:id>', methods=['POST'])
def editar_mysql(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET nombre = %s, mail = %s WHERE id_usuario = %s", 
                           (request.form['nombre'], request.form['mail'], id))
            conexion.commit()
        finally:
            cursor.close(); conexion.close()
    return redirect(url_for('admin_mysql'))

@app.route('/admin_productos_mysql')
def admin_productos_mysql():
    conexion = obtener_conexion()
    productos_db = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos")
            productos_db = cursor.fetchall()
        finally:
            cursor.close(); conexion.close()
    return render_template('admin_productos_mysql.html', productos=productos_db)

@app.route('/eliminar_producto_mysql/<int:id>')
def eliminar_producto_mysql(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
            conexion.commit()
        finally:
            cursor.close(); conexion.close()
    return redirect(url_for('admin_productos_mysql'))

@app.route('/editar_producto_mysql/<int:id>', methods=['POST'])
def editar_producto_mysql(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("UPDATE productos SET nombre = %s, precio = %s, cantidad = %s WHERE id_producto = %s", 
                           (request.form['nombre'], float(request.form['precio']), int(request.form['cantidad']), id))
            conexion.commit()
        finally:
            cursor.close(); conexion.close()
    return redirect(url_for('admin_productos_mysql'))

@app.route('/lista_usuarios_mysql')
def lista_usuarios_mysql():
    conexion = obtener_conexion()
    usuarios_db = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios"); usuarios_db = cursor.fetchall()
        finally:
            cursor.close(); conexion.close()
    return render_template('lista_usuarios.html', usuarios=usuarios_db)

# --- NUEVA RUTA PARA GUARDAR LA UBICACIÓN DESDE EL PANEL ---
@app.route('/guardar-ubicacion', methods=['POST'])
def guardar_ubicacion():
    if not session.get('usuario_id') or session.get('rol') != 'experto':
        return jsonify({"error": "No autorizado"}), 403
    
    datos = request.get_json()
    experto = Profesional.query.get(session['usuario_id'])
    
    if experto:
        experto.latitud = datos['lat']
        experto.longitud = datos['lng']
        db.session.commit()
        return jsonify({"mensaje": "📍 Ubicación actualizada con éxito"}), 200
    
    return jsonify({"error": "Experto no encontrado"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
    