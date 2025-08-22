import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)  # 50Hz for servo
        self.servo.start(0)

    def move(self, angle):
        # Clamp the angle to the range -90 to +90
        angle = max(min(angle, 90), -90)
        
        # Map angle (-90 to +90) to duty cycle (2.5 to 12.5)
        duty_cycle = 7.5 + (angle / 18)

        GPIO.output(self.pin, True)
        self.servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Shorter delay is usually sufficient
        GPIO.output(self.pin, False)
        self.servo.ChangeDutyCycle(0)

    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup()
