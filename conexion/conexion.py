import mysql.connector

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='', 
            database='inventario_db' # Verifica que este nombre sea igual en XAMPP
        )
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None