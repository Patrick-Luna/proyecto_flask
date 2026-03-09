import os
import json
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE RUTAS ---
# Usamos la carpeta principal para evitar errores de carpetas no encontradas
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Rutas de archivos de persistencia (Semana 12)
TXT_FILE = os.path.join(BASE_DIR, 'datos.txt')
JSON_FILE = os.path.join(BASE_DIR, 'datos.json')
CSV_FILE = os.path.join(BASE_DIR, 'datos.csv')

# --- CONFIGURACIÓN DE BASE DE DATOS (SQLite) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'inventario.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO DE DATOS ---
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

# --- RUTAS ---

@app.route('/')
def index():
    # Leemos desde SQLite para la tabla principal
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')

    if nombre and cantidad and precio:
        # 1. Guardar en SQLite
        nuevo = Producto(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        db.session.add(nuevo)
        db.session.commit()

        # 2. Persistencia en TXT (Modo append 'a')
        with open(TXT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"Producto: {nombre} | Cantidad: {cantidad} | Precio: {precio}\n")

        # 3. Persistencia en JSON
        datos_json = []
        if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
        datos_json.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, indent=4)

        # 4. Persistencia en CSV
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([nombre, cantidad, precio])

    return redirect(url_for('index'))

@app.route('/datos')
def ver_datos():
    # Ruta para cumplir el criterio de lectura de archivos
    lineas = []
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    return render_template('datos.html', contenido_txt=lineas)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    p = Producto.query.get(id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)