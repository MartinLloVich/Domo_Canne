import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import requests

# Pines y configuracion
LDR_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)

# Configuraion MQTT
MQTT_BROKER = "192.168.192.33"
MQTT_PORT = 1883
MQTT_TOPIC = "DomoCanne/comida_sensor"

# Configuraciion de alerta por correo
EMAIL_API_URL = "http://localhost:5000/send"
EMAIL_SENT = False
estado_anterior = None  # Para detectar cambios

def send_email():
    global EMAIL_SENT
    if not EMAIL_SENT:
        try:
            payload = {
                "to": "davidlaborda.2000@gmail.com",
                "subject": "Sin comida para el perro!",
                "message": "Se ha detectado que no queda comida en el recipiente del perro."
            }
            response = requests.post(EMAIL_API_URL, json=payload)
            if response.status_code == 200:
                print("Correo enviado con exito.")
                EMAIL_SENT = True
            else:
                print("Error en el servidor de correo:", response.text)
        except Exception as e:
            print("Fallo al contactar con el servidor de correo:", e)

# MQTT cliente
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    while True:
        luz_detectada = GPIO.input(LDR_PIN) == GPIO.HIGH
        estado_actual = "Sin comida" if luz_detectada else "Comida OK"

        if estado_actual != estado_anterior:
            print(f"Estado cambiado: {estado_actual}")
            client.publish(MQTT_TOPIC, estado_actual)
            estado_anterior = estado_actual

        if estado_actual == "Sin comida":
            send_email()
        else:
            EMAIL_SENT = False  # Reinicia alerta si vuelve a haber comida

        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
