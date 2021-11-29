import time
import paho.mqtt.client as paho
from paho import mqtt
from tkinter import *
from tkinter import ttk
import tkinter as tk



# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connection Success! Received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    topic = msg.topic
    payload = msg.payload
    if 'Crompton_Good' in topic:
        #print("Update Crompton Label: ",payload)
        Label(root, text = 'Crompton Production: '+str(payload) , font = 'arial 20 bold').place(x=40,y=200)
        
    elif 'Bosch_Good' in topic:
        #print("Update Bosch Label: ",payload)
        Label(root, text = 'Bosch Production: '+str(payload), font = 'arial 20 bold').place(x=40,y=80)
    root.update()
    

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("industry4.0", "Qwerty@123")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("1d1587d792b6466fa8f2db432d9d3db2.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("sensor1/#", qos=0)

root = Tk()
root.geometry('1000x500')
#production_name = input("Production Name(Eg: Bulb/Indicator/Housing/Electrical): ")
Label(root, text = 'Assembly Unit' , font = 'arial 20 bold').pack()

#ttk.Button(root, text="Quit", command=root.destroy).place(x=450,y=450)
client.loop_forever()



