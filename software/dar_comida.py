import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Pines GPIO usados
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
PINS = [IN1, IN2, IN3, IN4]

# Secuencia Half-Step (mas suave y precisa)
SEQ = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Configuracion GPIO
GPIO.setmode(GPIO.BCM)
for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Configuracion MQTT
MQTT_BROKER = "192.168.192.33"  # Cambia si usas otro broker/IP
MQTT_TOPIC = "DomoCanne/dar_comida"

def step_motor(steps, delay=0.002):
    """Mueve el motor la cantidad de pasos deseada"""
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    for _ in range(steps):
        for step in range(8)[::direction]:
            for pin in range(4):
                GPIO.output(PINS[pin], SEQ[step][pin])
            time.sleep(delay)

def mover_y_volver():
    print("? Dispensando comida...")
    pasos_por_vuelta = 480  # 360 grados del 28BYJ-48
    pasos_90 = pasos_por_vuelta // 4  # 90 grados
    step_motor(pasos_90)
    time.sleep(3)  # Espera 10 segundos
    print("?? Volviendo a posicion inicial...")
    step_motor(-pasos_90)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("? Conectado al broker MQTT")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print("? Mensaje recibido:", msg.payload.decode())
    if msg.payload.decode().lower() == "dar":
        mover_y_volver()

# Cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
