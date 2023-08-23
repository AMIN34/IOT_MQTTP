from django.shortcuts import render
from paho.mqtt.client import Client
import time


# Callback when a connection is established with the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed with return code", rc)

# Callback when a message is published
def on_publish(client, userdata, mid):
    print("Message published")

# Create a MQTT client instance
mqtt_client = Client(client_id="mqttx_22082023")
# mqtt_client = Client(client_id="mqttx_4ecc8cac")
mqtt_client.username_pw_set(username="TestIO", password="TestMQTT")

# Set callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

# Connect to the broker (using broker.emqx.io and port 1883)
broker_address = "broker.emqx.io"
port = 1883
mqtt_client.connect(broker_address, port, 60)

# Start the network loop in a blocking manner
mqtt_client.loop_start()
time.sleep(1)

# Create your views here.
def control_led(request):
    if request.method == 'POST':
        choice = int(request.POST.get('choice', 0))
        if choice:
            mqtt_client.publish("TestMQTT", "LED/ON")
        else:
            mqtt_client.publish("TestMQTT", "LED/OFF")
    return render(request, 'controller.html')

