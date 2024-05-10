from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:class_id>/', consumers.ChatRoomConsumer.as_asgi()),
]
