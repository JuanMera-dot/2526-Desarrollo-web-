import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',       # Usuario por defecto en XAMPP
            password='',       # XAMPP no usa contraseña por defecto, se deja vacío
            database='easy_home_db'
        )
        if conexion.is_connected():
            print("¡Conexión exitosa a la base de datos de Easy Home!")
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Este pedacito nos sirve para probar si funciona al ejecutar solo este archivo
if __name__ == '__main__':
    obtener_conexion()
    