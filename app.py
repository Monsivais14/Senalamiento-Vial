import sensors
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

zn = ZoneInfo('America/Matamoros')

# Inicializa las variables con valores predeterminados (por ejemplo, None o algún valor)
hum_ant = None
temp_ant = None

while True:
    try:
        hora_actual = datetime.now(zn)
        fecha_actual = hora_actual.date()  # Guarda solo la fecha
        hora = hora_actual.strftime("%H:%M")  # Formato HH:MM
        
        # Obtiene los valores del sensor
        hum, temp = sensors.GetResult(6)

        # Verifica si los valores son cero y no actualiza si lo son
        if hum == 0:
            hum = hum_ant  # Mantiene el valor anterior si es cero
        else:
            hum_ant = hum  # Actualiza el valor anterior si es válido

        if temp == 0:
            temp = temp_ant  # Mantiene el valor anterior si es cero
        else:
            temp_ant = temp  # Actualiza el valor anterior si es válido

        print(f"Hora: {hora}, Fecha: {fecha_actual}, Sensor: Hum: {hum}, Temp: {temp}")
        time.sleep(3)

    except KeyboardInterrupt:
        sys.exit(0)
