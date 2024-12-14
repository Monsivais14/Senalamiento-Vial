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

@app.route('/base', methods=['POST'])
def receive_json():
    try:
        # Obtener el JSON del cuerpo de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionó JSON en la solicitud"}), 400

        # Debugging
        print("JSON recibido:", data)

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

            print(f"Fecha: {fecha_actual}, Hora: {hora}, Sensor: Hum: {hum}, Temp: {temp}, Lluvia: {lluv}")
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
