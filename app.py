from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acerca')
def about():
    return render_template('about.html')

# Ruta dinámica - Semana 9
@app.route('/negocio/<item>')
def negocio(item):
    return render_template('index.html', mensaje=f"Consulta de: {item} exitosa")

if __name__ == '__main__':
    app.run(debug=True)