from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

import uuid
from datetime import datetime

class ChatRoom(models.Model):
    room_id = models.CharField(max_length=10, default=str(uuid.uuid4())[:10])
    members = models.ManyToManyField(User, related_name="room_members", blank=True)
    admin = models.ForeignKey(User, related_name="chatroom_admin", on_delete=models.CASCADE)
    online = models.ManyToManyField(User, related_name="room_online", blank=True)
    last_active = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.room_id

class Message(models.Model):
    user = models.ForeignKey(User, related_name="message_user", on_delete=models.CASCADE)
    to = models.ForeignKey(ChatRoom, related_name="message_room", on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}_to_{self.to.room_id}_{datetime.timestamp(self.created)}"