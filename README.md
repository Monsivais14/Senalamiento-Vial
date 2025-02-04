# Senalamiento Vial Inteligente programable para diferentes entornos 

## Descripción
Este repositorio es un proyecto presentado en la feria de Femeci Coahuila 2024, el cual fue ganador del primero lugar en la categoria de sistemas informaticos, la patente de este proyecto esta en proceso.

## Objetivo 
Diseñar y construir el prototipo a escala para la muestra del sistema propuesto de tal forma que se pueda llevar a construcción a escala normal.

## Características
- Internet de las Cosas (IoT)
- Integración de pagina web moderna
- Variedad de señalamientos
- Adaptabilidad del señalamiento a cambios ambientales
- Funciona con Temperatura, Humedad, Lluvia y Rango de horas

## Materiales
- Orange Pi Zero 3 (Debian 12)
- DHT11
- Raindrop sensor
- LED
- Resistencia

## Imagen del circuito
![Circuito del proyecto](/Circuito.png)


## Instalación y uso
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-proyecto.git
   ```
2. Accede a la carpeta:
   ```bash
   cd Senalamiento-Vial/
   ```
3. Ejecuta el Backend
   ```bash
   sudo Python3 app.py
   ```
4. Conectate con VSC usando SSH al orange pi y abre base.html con Open Live Server
5. Entra a la ruta que despliega el Backend en pantalla para obtener acceso a la pagina web
6. Configura el señalamiento

## Justificación
Este proyecto es crucial para abordar la falta de cultura vial y adaptar la señalización vial a los cambios climáticos y situaciones específicas en las carreteras. En la actualidad, no existen señalamientos viales eficientes que se actualicen inteligentemente para reducir la velocidad máxima permitida durante condiciones climáticas adversas como la lluvia o la niebla, una tarea esencial para prevenir accidentes.
La capacidad de programar señalizaciones preventivas, restrictivas, informativas y turísticas brinda versatilidad a la señalización vial, mejorando la seguridad en áreas específicas. Por ejemplo, en una carretera con construcción, el letrero se encargará de notificar la disminución de velocidad y mostrar la señal de obra en construcción. En una zona escolar, podría notificar la reducción de velocidad durante las horas de entrada y salida escolar y mostrar señalización de cruce peatonal o zona escolar.

## Futuras Mejoras
- Uso de paneles solares para alimentar los dispositivos y hacerlos más sostenibles.
- Expansión del sistema con más sensores para detectar otros factores ambientales como viento y visibilidad.
- Integración con sistemas municipales de control de tráfico para sincronización en tiempo real.
- Mejoras en la interfaz de usuario para hacerla más intuitiva y accesible.
