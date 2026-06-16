from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Crear base de datos y tabla
def crear_bd():
    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    whatsapp TEXT,
    correo TEXT,
    aeropuerto TEXT,
    destino TEXT,
    vuelo TEXT,
    fecha TEXT,
    hora TEXT,
    pasajeros INTEGER,
    observaciones TEXT,
    oferta REAL
)
""")

    conexion.commit()
    conexion.close()

crear_bd()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/reserva", methods=["POST"])
def reserva():

    nombre = request.form["nombre"]
    whatsapp = request.form["whatsapp"]
    correo = request.form["correo"]
    aeropuerto = request.form["aeropuerto"]
    destino = request.form["destino"]
    vuelo = request.form["vuelo"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    pasajeros = request.form["pasajeros"]
    observaciones = request.form["observaciones"]
    oferta = request.form["oferta"]

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO reservas
    (nombre, whatsapp, correo, aeropuerto, destino, vuelo, fecha, hora, pasajeros, observaciones, oferta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nombre,
        whatsapp,
        correo,
        aeropuerto,
        destino,
        vuelo,
        fecha,
        hora,
        pasajeros,
        observaciones,
        oferta
    ))

    conexion.commit()
    conexion.close()

    return f"""
    <h1>Reserva Guardada</h1>

    <p>Cliente: {nombre}</p>

    <p>Oferta: USD {oferta}</p>

    <a href='/'>
        Volver
    </a>
    """
@app.route("/reservas")
def reservas():

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM reservas")

    datos = cursor.fetchall()

    conexion.close()

    html = "<h1>Reservas Recibidas</h1>"

    for fila in datos:

        html += f"""
        <hr>
        ID: {fila[0]}<br>
        Cliente: {fila[1]}<br>
        WhatsApp: {fila[2]}<br>
        Aeropuerto: {fila[3]}<br>
        Destino: {fila[4]}<br>
        Vuelo: {fila[5]}<br>
        Oferta: USD {fila[6]}<br>
        """

    html += "<br><a href='/'>Volver</a>"

    return html

if __name__ == "__main__":
    app.run(debug=True)