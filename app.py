from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_segura_123"

# =========================
# BASE DE DATOS
# =========================
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

        oferta_cliente REAL,
        contraoferta_conductor REAL,

        estado TEXT,

        lat_origen REAL,
        lng_origen REAL,
        lat_destino REAL,
        lng_destino REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conductores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        usuario TEXT UNIQUE,
        password TEXT
    )
    """)

    conexion.commit()
    conexion.close()

crear_bd()

# =========================
# INICIO
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")

# =========================
# REGISTRO CONDUCTOR
# =========================
@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO conductores (nombre, usuario, password)
        VALUES (?, ?, ?)
        """, (
            request.form["nombre"],
            request.form["usuario"],
            request.form["password"]
        ))

        conexion.commit()
        conexion.close()

        return redirect("/login")

    return render_template("registro.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id FROM conductores
        WHERE usuario=? AND password=?
        """, (
            request.form["usuario"],
            request.form["password"]
        ))

        user = cursor.fetchone()
        conexion.close()

        if user:
            session["conductor_id"] = user[0]
            return redirect("/conductor")

        return "Login incorrecto"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

def login_required():
    return session.get("conductor_id")

# =========================
# RESERVA (CLIENTE)
# =========================
@app.route("/reserva", methods=["POST"])
def reserva():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO reservas (
        nombre, whatsapp, correo, aeropuerto, destino, vuelo,
        fecha, hora, pasajeros, observaciones,
        oferta_cliente, contraoferta_conductor,
        estado,
        lat_origen, lng_origen, lat_destino, lng_destino
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form["nombre"],
        request.form["whatsapp"],
        request.form["correo"],
        request.form["aeropuerto"],
        request.form["destino"],
        request.form["vuelo"],
        request.form["fecha"],
        request.form["hora"],
        request.form["pasajeros"],
        request.form["observaciones"],
        request.form["oferta"],
        None,
        "pendiente",
        request.form.get("lat_origen"),
        request.form.get("lng_origen"),
        request.form.get("lat_destino"),
        request.form.get("lng_destino")
    ))

    conexion.commit()
    conexion.close()

    return redirect("/")

# =========================
# PANEL CONDUCTOR
# =========================
@app.route("/conductor")
def conductor():

    if not login_required():
        return redirect("/login")

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()

    conexion.close()

    return render_template("conductor.html", reservas=reservas)

# =========================
# CONTRAOFERTA CONDUCTOR
# =========================
@app.route("/oferta_conductor/<int:id>", methods=["POST"])
def oferta_conductor(id):

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    UPDATE reservas
    SET contraoferta_conductor=?, estado='negociando'
    WHERE id=?
    """, (
        request.form["precio"],
        id
    ))

    conexion.commit()
    conexion.close()

    return redirect("/conductor")

# =========================
# ACEPTAR
# =========================
@app.route("/aceptar/<int:id>")
def aceptar(id):

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    UPDATE reservas
    SET estado='aceptado'
    WHERE id=?
    """, (id,))

    conexion.commit()
    conexion.close()

    return redirect("/conductor")

if __name__ == "__main__":
    app.run()