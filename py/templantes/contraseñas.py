import os

from flask import Flask, render_template, request, send_file

app = Flask(__name__)

def generar_passwords_sencillas(mascota, familia, edad, ciudad):
    """Genera contraseñas simples a partir de datos personales"""
    contras = [
        mascota + edad,
        familia + "123",
        ciudad + edad,
        mascota + "2025",
        familia + mascota,
        edad + ciudad,
        mascota + "01",
        familia + "00",
        ciudad + mascota
    ]
    return contras

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mascota = request.form["mascota"]
        familia = request.form["familia"]
        edad = request.form["edad"]
        ciudad = request.form["ciudad"]

        sugerencias = generar_passwords_sencillas(mascota, familia, edad, ciudad)

        # Guardar en fichero
        filename = "passwords.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== Contraseñas sugeridas (NO SEGURAS) ===\n")
            for p in sugerencias:
                f.write(p + "\n")

        return send_file(filename, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

