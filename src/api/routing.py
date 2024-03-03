from django.urls import re_path
from api import consumers

websocket_urlpattern = [
    re_path(r'ws/system_info/',consumers.SystemInfoConsumer.as_asgi())
]