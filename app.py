import os, json, csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración SQLite
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inventario.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)

# Rutas de los archivos (Semana 12)
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inventario', 'data')
TXT_FILE = os.path.join(DATA_DIR, 'datos.txt')
JSON_FILE = os.path.join(DATA_DIR, 'datos.json')
CSV_FILE = os.path.join(DATA_DIR, 'datos.csv')

# Modelo de Datos (POO)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float)

# Crear BD
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    # 1. Guardar en SQLite
    nuevo = Producto(nombre=nombre, precio=float(precio))
    db.session.add(nuevo)
    db.session.commit()

    # 2. Guardar en TXT
    with open(TXT_FILE, 'a') as f:
        f.write(f"Producto: {nombre}, Precio: {precio}\n")

    # 3. Guardar en JSON
    datos_json = []
    if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
        with open(JSON_FILE, 'r') as f:
            datos_json = json.load(f)
    datos_json.append({"nombre": nombre, "precio": precio})
    with open(JSON_FILE, 'w') as f:
        json.dump(datos_json, f, indent=4)

    # 4. Guardar en CSV
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, precio])

    return redirect(url_for('index'))

# NUEVA RUTA SEMANA 12 para ver los archivos
@app.route('/datos')
def ver_datos():
    # Leer TXT
    contenido_txt = ""
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, 'r') as f:
            contenido_txt = f.readlines()
    
    return render_template('datos.html', txt=contenido_txt)