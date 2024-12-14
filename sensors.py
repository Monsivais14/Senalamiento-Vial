import wiringpi
from wiringpi import GPIO

wiringpi.wiringPiSetup()

# Inicializa las variables con valores predeterminados
hum_ant = 0.1  # Valor predeterminado para la humedad
temp_ant = 20.0  # Valor predeterminado para la temperatura

def getval(pin):
    tl = []
    tb = []
    wiringpi.pinMode(pin, GPIO.OUTPUT)
    wiringpi.digitalWrite(pin, GPIO.HIGH)
    wiringpi.delay(1)
    wiringpi.digitalWrite(pin, GPIO.LOW)
    wiringpi.delay(25)
    wiringpi.digitalWrite(pin, GPIO.HIGH)
    wiringpi.delayMicroseconds(20)
    wiringpi.pinMode(pin, GPIO.INPUT)
    while(wiringpi.digitalRead(pin) == 1): pass
    
    for i in range(45):
        tc = wiringpi.micros()
        while(wiringpi.digitalRead(pin) == 0): pass
        while(wiringpi.digitalRead(pin) == 1):
            if wiringpi.micros() - tc > 500:
                break
        if wiringpi.micros() - tc > 500:
            break
        tl.append(wiringpi.micros() - tc)

    tl = tl[1:]
    for i in tl:
        if i > 100:
            tb.append(1)
        else:
            tb.append(0)
    
    return tb

# Método para obtener hum y temp
def GetResult(pin):
    global hum_ant, temp_ant  # Usa las variables globales

    # Inicializar las variables locales para los valores de los sensores
    for i in range(10):
        SH = 0
        SL = 0
        TH = 0
        TL = 0
        C = 0
        result = getval(pin)

        if len(result) == 40:
            for i in range(8):
                SH *= 2
                SH += result[i]    # humi Integer
                SL *= 2
                SL += result[i + 8]  # humi decimal
                TH *= 2
                TH += result[i + 16] # temp Integer
                TL *= 2
                TL += result[i + 24] # temp decimal
                C *= 2
                C += result[i + 32]   # Checksum

            if ((SH + SL + TH + TL) % 256) == C and C != 0:
                break
            else:
                break
        else:
            break
        wiringpi.delay(200)

    # Calcular flotante_1 y flotante_2
    hum = float(f"{SH}.{SL}")
    temp = float(f"{TH}.{TL}")

    # Verifica si los valores son cero o fuera de rango y no actualiza si lo son
    if hum == 0 or hum >= 100:
        hum = hum_ant  # Mantiene el valor anterior si es cero o fuera de rango
    else:
        hum_ant = hum  # Actualiza el valor anterior si es válido

    if temp == 0 or temp >= 100:
        temp = temp_ant  # Mantiene el valor anterior si es cero o fuera de rango
    else:
        temp_ant = temp  # Actualiza el valor anterior si es válido
    
    return hum, temp

# Método para obtener la lluvia 
def getLluvia(pin): 
    wiringpi.pinMode(pin, GPIO.INPUT)  # Lee el valor del pin (HIGH o LOW)
    return wiringpi.digitalRead(pin) != GPIO.HIGH
