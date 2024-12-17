import sensors
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import tkinter as tk
import socket
from PIL import Image, ImageTk

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS
zn = ZoneInfo('America/Matamoros')  # Zona horaria

# Pines de sensores GPIO wPI
dhtPin = 6  # Physical 12
lluvPin = 9  # Physical 16
led = 10  # Physical 18

# Variables globales
class AppState:
    def __init__(self):
        self.typeBase = None
        self.typeCondicional = None
        self.nameBase = None
        self.nameCondicional = None
        self.temperature = None
        self.humidity = None
        self.horaInicio = None
        self.horaFin = None
        self.lluvia = None
        self.window = None
        self.label = None
        self.image_label = None  # Añadir etiqueta para la imagen

state = AppState()

# Función para obtener la IP del dispositivo
def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Función para actualizar la interfaz
def actualizar_interfaz():
    if state.window:
        ip = obtener_ip()

        # Si no se ha recibido 'typeBase' y 'nameBase', mostrar texto
        if state.typeBase is None:
            texto = f"{ip}:5500/templates/base"
        else:
            texto = f"{ip}:5500/cambio/base\n\n"
            texto += f"Type Base: {state.typeBase}\n"
            texto += f"Name Base: {state.nameBase}\n"
            # Mostrar la imagen correspondiente
            imagen_path = f"static/{state.nameBase}.webp"
            
            try:
                img = Image.open(imagen_path)

                # Obtener las dimensiones de la ventana
                window_width = state.window.winfo_width()
                window_height = state.window.winfo_height()

                # Mantener la proporción de la imagen
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height

                if window_width / window_height > aspect_ratio:
                    # Si la relación de aspecto de la ventana es mayor que la de la imagen
                    new_width = int(window_height * aspect_ratio)
                    new_height = window_height
                else:
                    # Si la relación de aspecto de la ventana es menor que la de la imagen
                    new_width = window_width
                    new_height = int(window_width / aspect_ratio)

                # Redimensionar la imagen manteniendo la proporción
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

                img_tk = ImageTk.PhotoImage(img)

                # Si no existe la etiqueta de la imagen, crearla
                if not state.image_label:
                    state.image_label = tk.Label(state.window, image=img_tk)
                    state.image_label.image = img_tk  # Guardar referencia para que no se elimine
                    state.image_label.pack(fill=tk.BOTH, expand=True)
                else:
                    # Actualizar la imagen de la etiqueta
                    state.image_label.configure(image=img_tk)
                    state.image_label.image = img_tk  # Actualizar la referencia de la imagen

                # Eliminar la etiqueta de texto si ya está visible
                if state.label:
                    state.label.destroy()
                    state.label = None

            except FileNotFoundError:
                texto += "\nImagen no encontrada."

            if state.typeCondicional:
                texto += f"\nType Condicional: {state.typeCondicional}\n"
                texto += f"Name Condicional: {state.nameCondicional}\n"
                texto += f"Temperature: {state.temperature}°C\n"
                texto += f"Humidity: {state.humidity}%\n"
                texto += f"Hora Inicio: {state.horaInicio}\n"
                texto += f"Hora Fin: {state.horaFin}\n"
                texto += f"Lluvia: {'Sí' if state.lluvia else 'No'}"
        
        # Actualizar texto si no se muestra imagen
        if not state.image_label:
            state.label.config(text=texto)
        state.window.update()


@app.route('/base', methods=['POST'])
def receive_json():
    try:
        # Obtener el JSON del cuerpo de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionó JSON en la solicitud"}), 400

        # Debugging
        print("JSON recibido:", data)
        
        for i in range(5):
            sensors.parpadeo(led)

        type = data['type']
        # Clasifica y guarda los datos dependiendo del tipo de señalamiento
        if(type == 'base'):
            state.typeBase = type
            state.nameBase = data['name']
        else:
            state.typeCondicional = type
            state.nameCondicional = data['name']
            state.temperature = data['temperature']
            state.humidity = data['humidity']
            state.horaInicio = data['horaInicio']
            state.horaFin = data['horaFin']
            state.lluvia = data['lluvia']

        # Actualizar la interfaz
        actualizar_interfaz()

        return jsonify({"message": "JSON recibido con éxito", "content": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

def sensor_loop():
    while True:
        try:
            hora_actual = datetime.now(zn)
            fecha_actual = hora_actual.date()
            hora = hora_actual.strftime("%H:%M")

            # Obtiene los valores de los sensores
            hum, temp = sensors.GetResult(dhtPin)
            lluv = sensors.getLluvia(lluvPin)
            sensors.parpadeo(led)

            print(f"\nFecha: {fecha_actual}, Hora: {hora}")
            print(f"Sensor: Hum: {hum}, Temp: {temp}, Lluvia: {lluv}")
            print(f"Estado actual:")
            print(f"typeBase: {state.typeBase}, typeCondicional: {state.typeCondicional}")
            print(f"nameBase: {state.nameBase}, nameCondicional: {state.nameCondicional}")
            print(f"temperature: {state.temperature}, humidity: {state.humidity}")
            print(f"horaInicio: {state.horaInicio}, horaFin: {state.horaFin}")
            print(f"lluvia: {state.lluvia}")

            time.sleep(1)
        except Exception as e:
            print(f"Error en la lectura de sensores: {e}")

def interfaz_grafica():
    # Configurar la ventana
    state.window = tk.Tk()
    state.window.title("Interfaz de IP")
    state.window.configure(bg="black")
    state.window.attributes("-fullscreen", True)

    # Configurar el texto
    state.label = tk.Label(
        state.window,
        text="Iniciando...",
        fg="white",
        bg="black",
        font=("Arial", 40),
        justify=tk.LEFT
    )
    state.label.pack(expand=True)

    # Actualizar la interfaz inicial
    actualizar_interfaz()

    # Cerrar ventana con Escape
    state.window.bind("<Escape>", lambda e: state.window.destroy())
    state.window.mainloop()

if __name__ == '__main__':
    try:
        # Iniciar Flask en un hilo separado
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Iniciar ciclo de sensores en un hilo separado
        sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
        sensor_thread.start()

        # Iniciar la interfaz gráfica
        interfaz_grafica()
    except KeyboardInterrupt:
        print("Ejecución interrumpida por el usuario.")
        sys.exit(0)
