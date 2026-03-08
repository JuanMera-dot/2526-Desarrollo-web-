import sqlite3

def conectar_db():
    return sqlite3.connect('easyhome.db')

def crear_tablas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # TABLA UNIFICADA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    
    # Tabla de trabajadores 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trabajadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profesion TEXT,
            ubicacion TEXT,
            proposito TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

class Producto:
    def __init__(self, id, nombre, cantidad, precio, categoria):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.categoria = categoria

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto):
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?)
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.categoria))
        conexion.commit()
        conexion.close()

    def cargar_desde_db(self):
        self.productos = {}
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM productos')
        for fila in cursor.fetchall():
            p = Producto(*fila)
            self.productos[p.id] = p
        conexion.close()

        
