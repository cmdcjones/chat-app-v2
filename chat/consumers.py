import json
from datetime import datetime
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = parse_qs(self.scope['query_string'].decode()).get('token', None)
        if token is None:
            await self.close()
            return
        try:
            decoded_token = UntypedToken(token[0])
            user = await sync_to_async(User.objects.get)(id=decoded_token.payload['user_id'])
            self.scope['user'] = user
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            messages = await self.get_messages()
            for message in messages:
                await self.send(text_data=json.dumps({
                    'message': message['content'],
                    'sender': message['sender'],
                    'timestamp': message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                }))
        except:
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except:
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = data['sender']
        type = data['type']
        if type == "chat_message":
            message = data['message']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await self.save_message(room_name=self.room_name, sender=sender, content=message)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': type,
                    'message': message,
                    'sender': sender,
                    'timestamp': timestamp
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': type,
                    'sender': sender,
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

    async def started_typing(self, event):
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'type': "started_typing",
            'sender': sender
        }))

    async def stopped_typing(self, event):
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'type': "stopped_typing",
            'sender': sender
        }))

    async def save_message(self, room_name, sender, content):
        await Message.objects.acreate(room_name=room_name, sender=sender, content=content)

    async def get_messages(self):
        messages = await sync_to_async(lambda: list(Message.objects.filter(room_name=self.room_name).order_by('timestamp')[:50].values()))()
        return messages