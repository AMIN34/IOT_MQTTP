# django
from django.shortcuts import render
from django.views import View
from django.shortcuts import render

#internal
from .models import LEDClients
import time
import json
# third party
from paho.mqtt.client import Client


class MQTTClient:
    def __init__(self, client_id, username, password):
        self.client = Client(client_id=client_id)
        self.client.username_pw_set(username=username, password=password)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.connect("broker.emqx.io", 1883, 60)
        
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.client.loop_start()
        
            # self.client.loop_stop()
        else:
            print("Failed to connect to broker with return code: ", rc)
    
    def on_publish(self, client, userdata, mid):
        time.sleep(1)
        print("Message published to broker")
    
    def publish(self, topic, message):
        self.client.publish(topic, message, qos=0)
        self.client.loop_stop()
        

        
class ControlLEDView(View):
    template_name = 'controller.html'
    
    def get_context_data(self, **kwargs):
        return {"led_clients": LEDClients.objects.all()}
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        choice = int(request.POST.get('choice', 0))
        if led_client_id := request.POST.get('led_client_id'):
            led_client = LEDClients.objects.get(id = led_client_id)
            mqtt_client = MQTTClient(led_client.client_id, "TestIO", "TestMQTT")
            status = {1: "ON", 0: "OFF"}
            mqtt_client.publish("TestMQTT",json.dumps({"id": led_client.client_id, "status":"LED/"+status[choice]}))
            led_client.led_state = choice
            # if choice:
            #     mqtt_client.publish("TestMQTT",json.dumps({"id": led_client_id, "status":status[choice]}))
            #     led_client.led_state = True
            # else:
            #     mqtt_client.publish("TestMQTT",json.dumps({"id": led_client_id, "status":status[choice]}))
            #     led_client.led_state = False
            led_client.save()

        return render(request, self.template_name, self.get_context_data())



# import asyncio
# from django.shortcuts import render
# from django.views import View
# from asgiref.sync import sync_to_async
# from .models import LEDClients
# import time
# from paho.mqtt.client import Client

# class MQTTClient:
#     def __init__(self, client_id, username, password):
#         self.client = Client(client_id=client_id)
#         self.client.username_pw_set(username=username, password=password)
#         self.client.on_connect = self.on_connect
#         self.client.on_publish = self.on_publish

#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(self.connect())
        
#     async def connect(self):
#         await self.client.connect("broker.emqx.io", 1883, 60)
#         self.client.loop_start()
        
#     def on_connect(self, client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to broker")
#         else:
#             print("Failed to connect to broker with return code: ", rc)
    
#     def on_publish(self, client, userdata, mid):
#         time.sleep(1)
#         print("Message published to broker")
    
#     async def publish(self, topic, message):
#         await asyncio.sleep(0)  # Use asyncio.sleep to yield control to the event loop
#         self.client.publish(topic, message, qos=0)

# class ControlLEDView(View):
#     template_name = 'controller.html'
    
#     async def get_context_data(self, **kwargs):
#         return {"led_clients": await sync_to_async(LEDClients.objects.all)()}
    
#     async def get(self, request, *args, **kwargs):
#         return await render(request, self.template_name, await self.get_context_data())
    
#     async def post(self, request, *args, **kwargs):
#         choice = int(request.POST.get('choice', 0))
#         led_client_id = request.POST.get('led_client_id')
        
#         if led_client_id:
#             led_client = await sync_to_async(LEDClients.objects.get)(id=led_client_id)
#             mqtt_client = MQTTClient(led_client.client_id, "TestIO", "TestMQTT")
            
#             if choice:
#                 await sync_to_async(mqtt_client.publish)("TestMQTT", "LED/ON")
#                 led_client.led_state = True
#             else:
#                 await sync_to_async(mqtt_client.publish)("TestMQTT", "LED/OFF")
#                 led_client.led_state = False
            
#             await sync_to_async(led_client.save)()
        
#         return await render(request, self.template_name, await self.get_context_data())
