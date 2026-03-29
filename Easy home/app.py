from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from inventario import Inventario, Producto, crear_tablas, conectar_db
import sqlite3

# --- 1. IMPORTACIONES ---
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from fpdf import FPDF 
from werkzeug.security import generate_password_hash, check_password_hash

import json
import csv
import os
from datetime import datetime

from conexion.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = 'uea_tic_secret_2026'

# --- 2. CONFIGURACIÓN DE SQLALCHEMY ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easyhome_orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 3. MODELOS DE DATOS ---
class NuevoServicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    profesion = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    proposito = db.Column(db.Text, nullable=False)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    
    solicitudes = db.relationship('Solicitud', backref='experto', lazy=True)
    resenias = db.relationship('Resenia', backref='experto', lazy=True)

    def promedio_estrellas(self):
        if not self.resenias:
            return 0
        total = sum(r.estrellas for r in self.resenias)
        return round(total / len(self.resenias), 1)

class UsuarioCliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
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

@app.route('/buscar_experto')
def buscar_experto():
    query = request.args.get('q', '')
    if query:
        expertos_filtrados = Profesional.query.filter(
            or_(
                Profesional.profesion.ilike(f'%{query}%'),
                Profesional.proposito.ilike(f'%{query}%'),
                Profesional.nombre.ilike(f'%{query}%')
            )
        ).all()
    else:
        expertos_filtrados = Profesional.query.all()

    categorias_db = db.session.query(Profesional.profesion).distinct().all()
    lista_categorias = [c[0] for c in categorias_db]
    return render_template('expertos.html', categorias=lista_categorias, expertos=expertos_filtrados)

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
# GESTIÓN DE USUARIOS Y SEGURIDAD (CON ENCRIPTACIÓN)
# =========================================================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        password_encriptada = generate_password_hash(request.form['password'])
        nuevo_profesional = Profesional(
            nombre=request.form['nombre'], 
            correo=request.form['correo'],
            password=password_encriptada,
            profesion=request.form['profesion'],
            ubicacion=request.form['ubicacion'], 
            proposito=request.form['proposito']
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
        password_encriptada = generate_password_hash(request.form['password'])

        conexion_mysql = obtener_conexion()
        if conexion_mysql:
            try:
                cursor = conexion_mysql.cursor()
                sql = "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)"
                valores = (nombre_form, correo_form, password_encriptada)
                cursor.execute(sql, valores)
                conexion_mysql.commit()
            except Exception as e:
                print(f"Error guardando en MySQL: {e}")
            finally:
                cursor.close(); conexion_mysql.close()

        nuevo_cliente = UsuarioCliente(nombre=nombre_form, correo=correo_form, password=password_encriptada)
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
        if experto and check_password_hash(experto.password, clave):
            session.clear() 
            session['usuario_id'] = experto.id
            session['nombre_usuario'] = experto.nombre
            session['rol'] = 'experto'
            return redirect(url_for('index'))

        cliente = UsuarioCliente.query.filter_by(correo=id_user).first()
        if cliente and check_password_hash(cliente.password, clave):
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

@app.route('/portal-colaboradores', methods=['GET', 'POST'])
def portal_colaboradores():
    if request.method == 'POST':
        correo_login = request.form.get('correo')
        password_login = request.form.get('password')
        experto = Profesional.query.filter_by(correo=correo_login).first()
        if experto and check_password_hash(experto.password, password_login):
            session.clear() 
            session['usuario_id'] = experto.id
            session['nombre_usuario'] = experto.nombre
            session['rol'] = 'experto'
            flash(f'👋 Bienvenido de nuevo, {experto.nombre}.', 'success')
            return redirect(url_for('dashboard_colaborador')) 
        else:
            flash('❌ Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('portal_colaboradores'))
    return render_template('login_colaborador.html')

@app.route('/dashboard-colaborador', methods=['GET', 'POST'])
def dashboard_colaborador():
    if not session.get('usuario_id') or session.get('rol') != 'experto':
        return redirect(url_for('portal_colaboradores'))
    
    experto = Profesional.query.get(session['usuario_id'])

    if request.method == 'POST':
        nuevo_proposito = request.form.get('aspiraciones')
        if nuevo_proposito:
            experto.proposito = nuevo_proposito
            db.session.commit()
            flash('✅ Perfil actualizado correctamente.', 'success')
        return redirect(url_for('dashboard_colaborador'))

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

        conexion_mysql = obtener_conexion()
        if conexion_mysql:
            try:
                cursor = conexion_mysql.cursor()
                sql = "INSERT INTO productos (nombre, precio, cantidad, categoria) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre, precio, cantidad, categoria))
                conexion_mysql.commit()
            finally:
                cursor.close(); conexion_mysql.close()

        nuevo = Producto(None, nombre, cantidad, precio, categoria)
        inv.agregar_producto(nuevo)
        flash('📦 Producto añadido con éxito.', 'success')
        return redirect(url_for('admin'))

    inv.cargar_desde_db()
    return render_template('admin.html', productos=inv.productos.values())

@app.route('/borrar_producto_admin/<int:id>')
def borrar_producto_admin(id):
    if not session.get('es_admin'):
        return redirect(url_for('login'))

    nombre_borrado = inv.eliminar_producto(id)
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
        flash('🔒 Acceso restringido. Debes iniciar sesión como cliente.', 'warning')
        return redirect(url_for('login'))
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
    conexion = obtener_conexion(); usuarios_db = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios"); usuarios_db = cursor.fetchall()
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
    conexion = obtener_conexion(); productos_db = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos"); productos_db = cursor.fetchall()
        finally:
            cursor.close(); conexion.close()
    return render_template('admin_productos_mysql.html', productos=productos_db)

@app.route('/eliminar_producto_mysql/<int:id>')
def eliminar_producto_mysql(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(); cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
            conexion.commit()
        finally:
            cursor.close(); conexion.close()
    return redirect(url_for('admin_productos_mysql'))

@app.route('/editar_producto_mysql/<int:id>', methods=['POST'])
def editar_producto_mysql(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(); cursor.execute("UPDATE productos SET nombre = %s, precio = %s, cantidad = %s WHERE id_producto = %s", 
                           (request.form['nombre'], float(request.form['precio']), int(request.form['cantidad']), id))
            conexion.commit()
        finally:
            cursor.close(); conexion.close()
    return redirect(url_for('admin_productos_mysql'))

@app.route('/lista_usuarios_mysql')
def lista_usuarios_mysql():
    conexion = obtener_conexion(); usuarios_db = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True); cursor.execute("SELECT * FROM usuarios"); usuarios_db = cursor.fetchall()
        finally:
            cursor.close(); conexion.close()
    return render_template('lista_usuarios.html', usuarios=usuarios_db)

@app.route('/guardar-ubicacion', methods=['POST'])
def guardar_ubicacion():
    if not session.get('usuario_id') or session.get('rol') != 'experto': return jsonify({"error": "No autorizado"}), 403
    datos = request.get_json(); experto = Profesional.query.get(session['usuario_id'])
    if experto:
        experto.latitud, experto.longitud = datos['lat'], datos['lng']; db.session.commit()
        return jsonify({"mensaje": "📍 Ubicación actualizada"}), 200
    return jsonify({"error": "No encontrado"}), 404

# =========================================================
# GENERACIÓN DE REPORTES EN PDF
# =========================================================

# 1. REPORTE DE EXPERTOS
@app.route('/generar_reporte_pdf')
def generar_reporte_pdf():
    expertos_lista = Profesional.query.all()
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte de colaboradores - Easy Home", ln=True, align='C'); pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    # Encabezado azul para expertos
    pdf.set_fill_color(0, 168, 255); pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 10, 'Nombre', 1, 0, 'C', True); pdf.cell(60, 10, 'Profesion', 1, 0, 'C', True); pdf.cell(70, 10, 'Ubicacion', 1, 1, 'C', True)
    pdf.set_font("Arial", size=10); pdf.set_text_color(0, 0, 0)
    for e in expertos_lista:
        pdf.cell(60, 10, e.nombre.encode('latin-1', 'replace').decode('latin-1'), 1)
        pdf.cell(60, 10, e.profesion.encode('latin-1', 'replace').decode('latin-1'), 1)
        pdf.cell(70, 10, e.ubicacion.encode('latin-1', 'replace').decode('latin-1'), 1); pdf.ln()
    
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_expertos.pdf'
    return response

# 2. NUEVO: REPORTE DE PRODUCTOS (INVENTARIO)
@app.route('/generar_reporte_productos_pdf')
def generar_reporte_productos_pdf():
    inv.cargar_desde_db()
    productos = inv.productos.values()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte de Inventario - Easy Home", ln=True, align='C')
    pdf.ln(10)
    
    # Encabezado verde para productos
    pdf.set_fill_color(16, 185, 129); pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, 'Producto', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Categoria', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Stock', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Precio ($)', 1, 1, 'C', True)
    
    # Datos
    pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", size=10)
    for p in productos:
        pdf.cell(60, 10, str(p.nombre).encode('latin-1', 'replace').decode('latin-1'), 1)
        pdf.cell(50, 10, str(p.categoria).encode('latin-1', 'replace').decode('latin-1'), 1)
        pdf.cell(40, 10, str(p.cantidad), 1, 0, 'C')
        pdf.cell(40, 10, f"{p.precio:.2f}", 1, 1, 'C')
        
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_inventario.pdf'
    return response

if __name__ == '__main__':
    with app.app_context(): db.create_all() 
    app.run(debug=True)
    