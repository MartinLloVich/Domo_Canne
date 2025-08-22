import serial
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import math
import board
import servo_control  # Make sure you have a script to control the servo

# Pin configuration
TRIG = 23  # Trigger pin for the ultrasonic sensor
ECHO = 24
SERVO_PIN = 17          # GPIO17, physical pin 11
FAN_PIN = 18      # GPIO18, physical pin 12 (PWM capable)

# --- Temperature thresholds ---  
FAN_TEMP_THRESHOLD = 31.0
SERVO_TEMP_THRESHOLD = 33.0

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

door_open = False
# Safe mode variable
safe_mode = False

# --- Serial communication setup ---
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# --- MQTT setup ---
broker = "192.168.192.33"
topic_temp = "DomoCanne/temperatura"
topic_hum = "DomoCanne/humedad"
topic_safe_mode = 'DomoCanne/safe_mode'

# Functions
def measure_distance():
    # Send a 10us pulse to activate the ultrasonic sensor
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # Measure the time it takes to receive the pulse back
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def on_message(client, userdata, message):
    global safe_mode
    # Check the received message and activate/deactivate safe_mode
    if message.topic == topic_safe_mode:
        safe_mode = (message.payload.decode() == 'true')

# --- Servo control functions (using servo_control library) ---
def move_servo_90_degrees():
    # Control the servo motor to move to 90 degrees
    servo = servo_control.Servo(SERVO_PIN)
    servo.move(25)

def reposition_servo():
    # Return the servo motor to 0 degrees
    servo = servo_control.Servo(SERVO_PIN)
    servo.move(-18)

client = mqtt.Client()
client.connect(broker, 1883, 60)
client.on_message = on_message
client.subscribe(topic_safe_mode)

try:
    while True:
        
        client.loop()  # Listen for MQTT messages
        
        if not safe_mode:
            # If safe mode is not activated, monitor the ultrasonic sensor
            distance = measure_distance()
            print("Distance: {} cm".format(distance))

            # If there is an obstacle, move the servo
            if distance < 5:  # Distance threshold
                move_servo_90_degrees()
                time.sleep(5)  # Wait for 5 seconds
                reposition_servo()

        time.sleep(1)  # Wait for one second before repeating
        
        try:
            line = ser.readline().decode('latin1').strip()
            print("RAW:", line)
            if line.startswith('{'):
                data = json.loads(line)
                temp = float(data["temperature"])
                hum = float(data["humidity"])

                # Publish temperature and humidity
                client.publish(topic_temp, temp)
                client.publish(topic_hum, hum)

                # --- Control fan ---
                if temp > FAN_TEMP_THRESHOLD and temp < SERVO_TEMP_THRESHOLD:
                    GPIO.output(FAN_PIN, GPIO.HIGH)
                else:
                    GPIO.output(FAN_PIN, GPIO.LOW)

                # --- Control servo ---
                if temp > SERVO_TEMP_THRESHOLD and not door_open:
                    GPIO.output(FAN_PIN, GPIO.LOW)
                    time.sleep(1)
                    move_servo_90_degrees()
                    door_open = True
                elif temp < SERVO_TEMP_THRESHOLD and door_open:
                    GPIO.output(FAN_PIN, GPIO.LOW)
                    time.sleep(1)
                    reposition_servo()
                    door_open = False

        except Exception as e:
            print("Error:", e)

        time.sleep(1)  # Wait for one second before repeating

except KeyboardInterrupt:
    print("Program terminated")
    GPIO.cleanup()  # Clean up GPIO pin configurations
