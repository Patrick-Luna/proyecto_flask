from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def get(id_usuario, conexion):
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return Usuario(data['id_usuario'], data['nombre'], data['email'], data['password'])
        return None