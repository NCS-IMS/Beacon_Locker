# test BLE Scanning software
# jcs 6/8/2014
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import blescan
import sys
import bluetooth._bluetooth as bluez
import threading

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

relayPin = 16
openFlag = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relayPin, GPIO.OUT)

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
	if msg.topic == "uuid":
		userUUID = str(msg.payload.decode("utf-8"))
		thread = threading.Thread(target=startBeaconScanner, args=(userUUID,))
		thread.start()
		
	elif msg.topic =="test":
		if openFlag == True:
			thread.do_run = False
			GPIO.output(relayPin, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(relayPin, GPIO.LOW)
			openFlag = False
			

def startBeaconScanner(userUUID):
	global openFlag
	global thread
	while getattr(thread, "do_run", True):
		returnedList = blescan.parse_events(sock, 10)
		print("-----")
		for beacon in returnedList:
			s = beacon.split(",")
			if userUUID == s[1] and int(s[5]) >= -60 and openFlag == False:
				GPIO.output(relayPin, GPIO.HIGH)
				time.sleep(0.5)
				GPIO.output(relayPin, GPIO.LOW)
				openFlag = True
				thread.do_run = False
				print(s[1])


userUUID = ""
thread = ""
bleFlag = True
client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('localhost', 1883)
client.subscribe('uuid', 1)
client.subscribe('test', 2)
client.loop_forever()



