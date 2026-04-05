from conexion.conexion import obtener_conexion

class ProductoService:
    @staticmethod
    def listar_todos():
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        res = cursor.fetchall()
        db.close()
        return res

    @staticmethod
    def insertar(nombre, precio, stock):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", 
                       (nombre, precio, stock))
        db.commit()
        db.close()

    @staticmethod
    def obtener_por_id(id_p):
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        # Aquí usamos 'id' como está en tu phpMyAdmin
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_p,))
        res = cursor.fetchone()
        db.close()
        return res

    @staticmethod
    def actualizar(id_p, nombre, precio, stock):
        db = obtener_conexion()
        cursor = db.cursor()
        # Actualizamos usando la columna 'id'
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id=%s", 
                       (nombre, precio, stock, id_p))
        db.commit()
        db.close()

    @staticmethod
    def eliminar(id_p):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_p,))
        db.commit()
        db.close()