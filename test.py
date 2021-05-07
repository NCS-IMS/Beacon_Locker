import paho.mqtt.client as mqtt

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
    if msg.topic == "uuid":

    elif msg.topic == "":
        pass


client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('localhost', 1883)
client.subscribe('uuid', 1)
client.subscribe('test', 2)
client.loop_forever()
