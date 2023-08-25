from django.urls import path
from .views import ControlLEDView

urlpatterns = [
    path('', ControlLEDView.as_view(), name='control_led'),
]
