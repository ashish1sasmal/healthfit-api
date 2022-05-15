import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        type = data.get("type")
        from_ = data.get("from")
        msg = data.get("msg")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : "message",
                'type_' : type,
                'message' : data["msg"],
                'from' : from_
            }
        )

    async def message(self, event):
        await self.send(text_data=json.dumps({
            'type' : event['type_'],
            'message': event['message'],
            'from' : event['from']
        }))