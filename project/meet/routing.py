from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/message/<int:userid2>/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]