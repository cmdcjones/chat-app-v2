from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from datetime import datetime
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add( self.room_group_name, self.channel_name)
        await self.accept()
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'sender': message['sender'],
                'timestamp': message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await self.save_message(self.room_name, sender, message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
            }))

    @staticmethod
    async def save_message(room_name, sender, content):
        await Message.objects.acreate(room_name=room_name, sender=sender, content=content)

    async def get_messages(self):
        messages = await sync_to_async(lambda: list(Message.objects.filter(room_name=self.room_name).order_by('-timestamp')[:50].values()))()
        return messages