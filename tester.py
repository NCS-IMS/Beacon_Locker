import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

relayPin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relayPin, GPIO.OUT)

GPIO.output(relayPin, GPIO.LOW)
time.sleep(0.5)
GPIO.output(relayPin, GPIO.HIGH)

GPIO.cleanup()