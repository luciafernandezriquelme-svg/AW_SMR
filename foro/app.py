import sqlite3

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

def conectar():
    return sqlite3.connect("database/foro.db")

@app.route("/")
def index():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT temas.id, titulo, contenido, nombre FROM temas JOIN usuarios ON temas.autor_id = usuarios.id ORDER BY fecha DESC")
    temas = cursor.fetchall()
    conn.close()
    return render_template("index.html", temas=temas)

@app.route("/crear-tema", methods=["POST"])
def crear_tema():
    titulo = request.form["titulo"]
    contenido = request.form["contenido"]
    autor_id = 1  # temporal, luego se conecta con login
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temas (titulo, contenido, autor_id) VALUES (?, ?, ?)", (titulo, contenido, autor_id))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
    