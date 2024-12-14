import sensors
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS
zn = ZoneInfo('America/Matamoros') # Zona horaria 

# Pines de sensores GPIO wPI
dhtPin = 6 # Physical 12
lluvPin = 9 # Physical 16
led = 10 # Pyhusicak 18

# Inicializa las variables con valores predeterminados (por ejemplo, None o algún valor)
hum_ant = None
temp_ant = None

while True:
    try:
        hora_actual = datetime.now(zn)
        fecha_actual = hora_actual.date()  # Guarda solo la fecha
        hora = hora_actual.strftime("%H:%M")  # Formato HH:MM
        
        # Obtiene los valores de los sensores
        hum, temp = sensors.GetResult(dhtPin)
        lluv = sensors.getLluvia(lluvPin)

        # Verifica si los valores son cero y no actualiza si lo son
        if hum == 0:
            hum = hum_ant  # Mantiene el valor anterior si es cero
        else:
            hum_ant = hum  # Actualiza el valor anterior si es válido

        if temp == 0 or temp>=100:
            temp = temp_ant  # Mantiene el valor anterior si es cero
        else:
            temp_ant = temp  # Actualiza el valor anterior si es válido

        print(f"Hora: {hora}, Fecha: {fecha_actual}, Sensor: Hum: {hum}, Temp: {temp}, lluv: {lluv}")
        time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)
