import sensors
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS
zn = ZoneInfo('America/Matamoros')  # Zona horaria

# Pines de sensores GPIO wPI
dhtPin = 6  # Physical 12
lluvPin = 9  # Physical 16
led = 10    # Physical 18

typeBase = None
typeCondicional = None
nameBase = None
nameCondicional = None
temperature = None
humidity = None
horaInicio = None
horaFin = None
lluvia = None

@app.route('/base', methods=['POST'])
def receive_json():
    try:
        # Declarar las variables globales
        global typeBase, nameBase, typeCondicional, nameCondicional, temperature, humidity, horaInicio, horaFin, lluvia

        # Obtener el JSON del cuerpo de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionó JSON en la solicitud"}), 400

        # Debugging
        print("JSON recibido:", data)

        for i in range(5):
            sensors.parpadeo(led)

        type = data['type']

        # Clasifica y guarda los datos dependiendo del tipo de senalamiento
        if(type=='base'):
            typeBase = type
            nameBase = data['name']
        else:
            typeCondicional = type
            nameCondicional = data['name']
            temperature = data['temperature']
            humidity = data['humidity']
            horaInicio = data['horaInicio']
            horaFin = data['horaFin']
            lluvia = data['lluvia']

        # Devolver el contenido del JSON recibido
        return jsonify({"message": "JSON recibido con éxito", "content": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

def sensor_loop():
    while True:
        try:
            hora_actual = datetime.now(zn)
            fecha_actual = hora_actual.date()  # Guarda solo la fecha
            hora = hora_actual.strftime("%H:%M")  # Formato HH:MM

            # Obtiene los valores de los sensores
            hum, temp = sensors.GetResult(dhtPin)
            lluv = sensors.getLluvia(lluvPin)
            sensors.parpadeo(led)

            print(f" ")
            print(f"Fecha: {fecha_actual}, Hora: {hora}, Sensor: Hum: {hum}, Temp: {temp}, Lluvia: {lluv}")
            print(f"typeBase: {typeBase}, typeCondicional: {typeCondicional}, nameBase: {nameBase}, nameCondicional: {nameCondicional}, temperature: {temperature}, humidity: {humidity}, horaInicio: {horaInicio}, horaFin: {horaFin}, lluvia: {lluvia}")
            time.sleep(1)

        except Exception as e:
            print(f"Error en la lectura de sensores: {e}")

if __name__ == '__main__':
    try:
        # Ejecutar la aplicación Flask en un hilo separado
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Iniciar el bucle de sensores
        sensor_loop()

    except KeyboardInterrupt:
        print("Ejecución interrumpida por el usuario.")
        sys.exit(0)
