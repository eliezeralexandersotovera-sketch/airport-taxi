from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Airport Taxi RD</h1>
    <h2>Reserva tu traslado</h2>

    <form method="post" action="/reserva">

        <p>Nombre:</p>
        <input type="text" name="nombre">

        <p>WhatsApp:</p>
        <input type="text" name="whatsapp">

        <p>Aeropuerto:</p>
        <select name="aeropuerto">
            <option>PUJ - Punta Cana</option>
            <option>SDQ - Las Americas</option>
        </select>

        <p>Destino:</p>
        <input type="text" name="destino">

        <p>Numero de vuelo:</p>
        <input type="text" name="vuelo">

        <p>Oferta del pasajero (USD):</p>
        <input type="number" name="oferta">

        <br><br>

        <button type="submit">
            Solicitar Reserva
        </button>

    </form>
    """

@app.route("/reserva", methods=["POST"])
def reserva():

    nombre = request.form["nombre"]
    whatsapp = request.form["whatsapp"]
    aeropuerto = request.form["aeropuerto"]
    destino = request.form["destino"]
    vuelo = request.form["vuelo"]
    oferta = request.form["oferta"]

    return f"""
    <h1>Reserva Recibida</h1>

    <p><b>Cliente:</b> {nombre}</p>

    <p><b>WhatsApp:</b> {whatsapp}</p>

    <p><b>Aeropuerto:</b> {aeropuerto}</p>

    <p><b>Destino:</b> {destino}</p>

    <p><b>Vuelo:</b> {vuelo}</p>

    <p><b>Oferta:</b> USD {oferta}</p>

    <h3>Un conductor revisará la oferta.</h3>
    """

if __name__ == "__main__":
    app.run(debug=True)