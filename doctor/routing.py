from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/doctor/<str:doc_id>", consumers.DoctorConsumer.as_asgi()),
]
