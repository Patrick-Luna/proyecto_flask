from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from conexion.conexion import obtener_conexion
from models.usuario import Usuario 
from services.producto_service import ProductoService
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'patrick_luna_final_2026'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    db = obtener_conexion()
    u = Usuario.get(uid, db)
    db.close()
    return u

@app.route('/')
@login_required
def index():
    prods = ProductoService.listar_todos()
    cats = ProductoService.obtener_categorias()
    return render_template('productos/index.html', productos=prods, categorias=cats, usuario=current_user.nombre)

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    ProductoService.insertar(request.form['nombre'], request.form['precio'], 
                             request.form['stock'], request.form['id_categoria'])
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if request.method == 'POST':
        ProductoService.actualizar(id, request.form['nombre'], request.form['precio'], 
                                   request.form['stock'], request.form['id_categoria'])
        return redirect(url_for('index'))
    prod = ProductoService.obtener_por_id(id)
    cats = ProductoService.obtener_categorias()
    return render_template('productos/editar.html', producto=prod, categorias=cats, usuario=current_user.nombre)

@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    ProductoService.eliminar(id)
    return redirect(url_for('index'))

@app.route('/reporte_pdf')
@login_required
def reporte_pdf():
    productos = ProductoService.listar_todos()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "IMPORTADORA PATRICK LUNA - REPORTE FINAL", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(15, 10, "ID", 1); pdf.cell(70, 10, "Producto", 1); pdf.cell(35, 10, "Cat.", 1); pdf.cell(35, 10, "Stock", 1); pdf.cell(35, 10, "Precio", 1); pdf.ln()
    pdf.set_font("Arial", '', 10)
    for p in productos:
        pdf.cell(15, 10, str(p['id']), 1)
        pdf.cell(70, 10, str(p['nombre']), 1)
        pdf.cell(35, 10, str(p['nombre_categoria']), 1)
        pdf.cell(35, 10, str(p['stock']), 1)
        pdf.cell(35, 10, f"${p['precio']}", 1); pdf.ln()
    
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte_Final_Inventario.pdf'
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (request.form['email'], request.form['password']))
        user_data = cursor.fetchone()
        db.close()
        if user_data:
            user = Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'], user_data['password'])
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)