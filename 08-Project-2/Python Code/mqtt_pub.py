#This Program will check the room temperature 
#if Room Temperature Exceeds 30 Centigrade then it send the 
# Message at /gabjac-home/room/temperature to turn on the LED
# Else Turn Off the LED

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("/gabjac/room/temperature")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, message):
    readings=str(message.payload.decode("utf-8"))
    print("message received " ,readings)
    JsonReadings=json.loads(readings)
    print("Temperature=",JsonReadings["Temp"])
    if JsonReadings["Temp"]>30:
        client.publish("/gabjac/room/led","On")
    else:
        client.publish("/gabjac/room/led","Off")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
# client.username_pw_set(username="gabjac",password="temp123")
client.connect("167.172.87.186", 1883, 60)
# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()

