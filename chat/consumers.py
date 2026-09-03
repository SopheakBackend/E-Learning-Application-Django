import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, ):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
    
            
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data['message']
        now = timezone.now()
        await self.channel_layer.group_send (
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )
        await self.persist_message(message)
        
    async def persist_message(self, message):
                await Message.objects.acreate(
                    user = self.user, course_id = self.id, content = message
                )
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    
    
        
