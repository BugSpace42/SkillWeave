# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Проверяем, имеет ли пользователь доступ к комнате
        if not await self.user_can_access_room():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user_id = self.scope['user'].id

            # Save message to database
            await self.save_message(user_id, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': user_id,
                    'username': self.scope['user'].username
                }
            )
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, user_id, content):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            user = User.objects.get(id=user_id)
            Message.objects.create(room=room, sender=user, content=content)
        except ObjectDoesNotExist:
            pass

    @database_sync_to_async
    def user_can_access_room(self):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            return self.scope["user"] in room.participants.all()
        except ObjectDoesNotExist:
            return False