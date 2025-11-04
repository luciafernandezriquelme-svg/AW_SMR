import random
import string

from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templantes")

# Generador de contraseña a partir de datos personales
def generar_contraseñas(dni, mascota, hijos, nombre, hobies, padres):
    base = f"{dni}{mascota}{hijos}{nombre}{hobies}{padres}"
    contraseñas = []
    for _ in range(10):
        extras = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        contraseñas.append(base + extras)
    return contraseñas

# Generador de contraseña desde comando
def generar_contraseña_comando(comando):
    extras = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{comando}{extras}"

@app.route('/', methods=['GET', 'POST'])
def index():
    contraseñas = None
    color = request.form.get('color', '#222')
    fuente = request.form.get('fuente', 'Arial')
    if request.method == 'POST':
        dni = request.form.get('dni', '')
        mascota = request.form.get('mascota', '')
        hijos = request.form.get('hijos', '')
        nombre = request.form.get('nombre', '')
        hobies = request.form.get('hobies', '')
        padres = request.form.get('padres', '')
        contraseñas = generar_contraseñas(dni, mascota, hijos, nombre, hobies, padres)
    return render_template('plantilla.html', contraseñas=contraseñas, color=color, fuente=fuente)

@app.route('/comando', methods=['GET', 'POST'])
def comando_contraseña():
    contraseña = None
    if request.method == 'POST':
        comando = request.form.get('comando', '')
        contraseña = generar_contraseña_comando(comando)
    return render_template('comando_contraseña.html', contraseña=contraseña)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
