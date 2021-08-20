#-*- coding:utf-8 -*-
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import blescan
import sys
import bluetooth._bluetooth as bluez
import threading
import json, ast

def startBeaconScanner(uuidList):
	global openFlag
	global thread
	global thread2 #Flag controll
	while getattr(thread, "do_run", True):
		returnedList = blescan.parse_events(sock, 10)
		print("-----")
		for beacon in returnedList:
			s = beacon.split(",")
			print(s)
			if s[1] in uuidList and int(s[5]) >= -60 and openFlag == False:
				print(1111111111111111111111111111111)
				openDoor()				
				print(2222222222222222222222222222222)
				openFlag = True
				thread.do_run = False
				thread2 = threading.Thread(target=openController, args=())
				thread2.start()
				print(s[1])


def openController():
	global openFlag
	if openFlag == True:
		time.sleep(5)
		openFlag = False
		print("locker beacon Wait")

def openDoor():
	GPIO.output(relayPin, GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(relayPin, GPIO.HIGH)
	print("opendoor")

def on_connect(client, userdata, flag, rc):
    if rc == 0:
        print("connect OK")
    else:
        print("Bad Connection")

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " "+ str(granted_qos))

def on_message(client, userdata, msg):
	global thread
	global openFlag
	print(msg.topic)
	print(str(msg.payload.decode("utf-8")))
	
	if msg.topic == "uuid":
		uuidList = ast.literal_eval(msg.payload.decode("utf-8")) #디코딩
		thread = threading.Thread(target=startBeaconScanner, args=(uuidList,))
		thread.start()
		
	elif msg.topic =="close":
		if openFlag == True:
			thread.do_run = False
			GPIO.output(relayPin, GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(relayPin, GPIO.HIGH)
			openFlag = False



relayPin = 16
openFlag = False

userUUID = ""
thread = ""
thread2 = ""
bleFlag = True

dev_id = 0

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relayPin, GPIO.OUT, initial=GPIO.HIGH)

try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

try:
    client.connect('broker.mqtt-dashboard.com', 1883)
    client.subscribe('uuid', 1)
    client.subscribe('close', 2)
    client.loop_forever()
except:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()