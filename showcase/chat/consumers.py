import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message, OnlineStatus
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            user1 = self.scope['user'].username 
            user2 = self.room_name
            self.room_group_name = f"chat_{''.join(sorted([user1, user2]))}"
            
            await self.update_online_status(self.scope['user'], True)

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            # Handle the exception and close the WebSocket
            print(f"Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        
        # Update online status when user disconnects
        await self.update_online_status(self.scope['user'], False)
        
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']  
        receiver = await self.get_receiver_user() 

        await self.save_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            
            {
                'type': 'chat_message',
                'sender': sender.username,
                'receiver': receiver.username,
                'message': message
            }
        )
        

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message):
        Message.objects.create(sender=sender, receiver=receiver, content=message)

    @sync_to_async
    def get_receiver_user(self):
        return User.objects.get(username=self.room_name)
    
    @sync_to_async
    def update_online_status(self, user, is_online):
        # Update the user's online status
        online_status, created = OnlineStatus.objects.get_or_create(user=user)
        online_status.is_online = is_online
        online_status.last_seen = None if is_online else online_status.last_seen
        online_status.save()

