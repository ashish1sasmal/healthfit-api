from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('start/chat/', views.startRoom, name='startRoom'),
    path('chat/<str:room_id>', views.enterRoom, name='enterRoom'),
    path('delete/room/<str:room_id>', views.deleteRoom, name="deleteRoom"),
]
