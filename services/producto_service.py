from conexion.conexion import obtener_conexion

class ProductoService:
    @staticmethod
    def listar_todos():
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        # JOIN entre Productos y Categorías (Relación de tablas)
        query = """
            SELECT p.id, p.nombre, p.precio, p.stock, c.nombre_categoria 
            FROM productos p 
            INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        """
        cursor.execute(query)
        res = cursor.fetchall()
        db.close()
        return res

    @staticmethod
    def obtener_categorias():
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias")
        res = cursor.fetchall()
        db.close()
        return res

    @staticmethod
    def insertar(nombre, precio, stock, id_cat):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)", 
                       (nombre, precio, stock, id_cat))
        db.commit()
        db.close()

    @staticmethod
    def obtener_por_id(id_p):
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_p,))
        res = cursor.fetchone()
        db.close()
        return res

    @staticmethod
    def actualizar(id_p, nombre, precio, stock, id_cat):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s, id_categoria=%s WHERE id=%s", 
                       (nombre, precio, stock, id_cat, id_p))
        db.commit()
        db.close()

    @staticmethod
    def eliminar(id_p):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_p,))
        db.commit()
        db.close()