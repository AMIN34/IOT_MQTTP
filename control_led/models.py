from django.db import models
# Create your models here.

class LEDClients(models.Model):
    led_name = models.CharField(max_length=20)
    client_id = models.CharField(max_length=20)
    led_state = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.led_name} ( {self.client_id} )"
    