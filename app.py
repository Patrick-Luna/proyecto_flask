import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS (SQLite) ---
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inventario.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- PROGRAMACIÓN ORIENTADA A OBJETOS (POO) ---
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

# Crear la base de datos automáticamente al iniciar
with app.app_context():
    db.create_all()

# --- RUTAS DEL SISTEMA ---

@app.route('/')
def index():
    # Uso de Colecciones: Obtenemos todos los productos en una lista
    todos_los_productos = Producto.query.all()
    return render_template('index.html', productos=todos_los_productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    # Captura de datos del formulario
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))

    # Crear objeto y guardar en SQLite
    nuevo_producto = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
    db.session.add(nuevo_producto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    # Buscar por ID y eliminar
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)