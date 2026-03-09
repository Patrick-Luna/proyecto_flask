import os
import json
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE RUTAS Y PERSISTENCIA (Semana 12) ---
# Definimos las rutas para que funcionen tanto en tu PC como en Render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'inventario', 'data')

# Crear carpetas automáticamente si no existen para evitar errores
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Rutas de los archivos físicos
TXT_FILE = os.path.join(DATA_DIR, 'datos.txt')
JSON_FILE = os.path.join(DATA_DIR, 'datos.json')
CSV_FILE = os.path.join(DATA_DIR, 'datos.csv')

# --- CONFIGURACIÓN DE BASE DE DATOS (SQLite + ORM) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'inventario.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO DE DATOS (POO) ---
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

# Crear la base de datos al arrancar
with app.app_context():
    db.create_all()

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def index():
    # Leemos desde la Base de Datos (Persistencia SQLite)
    productos_db = Producto.query.all()
    return render_template('index.html', productos=productos_db)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')

    if nombre and cantidad and precio:
        # 1. Guardar en SQLite (SQLAlchemy)
        nuevo_p = Producto(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        db.session.add(nuevo_p)
        db.session.commit()

        # 2. Guardar en TXT (Usando open)
        with open(TXT_FILE, 'a') as f:
            f.write(f"ID: {nuevo_p.id} | Nombre: {nombre} | Cantidad: {cantidad} | Precio: {precio}\n")

        # 3. Guardar en JSON (Diccionarios)
        datos_json = []
        if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
            with open(JSON_FILE, 'r') as f:
                datos_json = json.load(f)
        
        datos_json.append({"id": nuevo_p.id, "nombre": nombre, "cantidad": cantidad, "precio": precio})
        
        with open(JSON_FILE, 'w') as f:
            json.dump(datos_json, f, indent=4)

        # 4. Guardar en CSV (Librería csv)
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['ID', 'Nombre', 'Cantidad', 'Precio'])
            writer.writerow([nuevo_p.id, nombre, cantidad, precio])

    return redirect(url_for('index'))

# NUEVA RUTA: Leer información de archivos (Semana 12)
@app.route('/datos')
def ver_datos():
    # Leer el archivo TXT para mostrarlo en HTML
    lineas_txt = []
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, 'r') as f:
            lineas_txt = f.readlines()
    
    return render_template('datos.html', contenido_txt=lineas_txt)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)