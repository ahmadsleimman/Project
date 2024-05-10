import json
import base64
from django.core.files.base import ContentFile
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from Course.models import Class, ClassMessage
from django.contrib.auth.models import User


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.class_id = self.scope['url_route']['kwargs']['class_id']
        self.room_group_name = f"chat_{self.class_id}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message_type = data['message_type']
        user = data['user']

        name = await self.get_name(user)

        if message_type == "message":
            body = data['body']
            await self.save_message(user=user, body=body)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': 'message',
                    'body': body,
                    'user': user,
                    'name': name,
                    'created': datetime.now().strftime("%b. %d, %Y, %I:%M %p")
                }
            )

        if message_type == "voice":
            voice = data['voice']
            voice_name = data['voice_name']

            decoded_voice = base64.b64decode(voice)
            content_file = ContentFile(decoded_voice, name=f"{voice_name}.mp3")

            await self.save_message(user=user, voice=content_file)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': 'voice',
                    'voice': voice,
                    'user': user,
                    'name': name,
                    'created': datetime.now().strftime("%b. %d, %Y, %I:%M %p")
                }
            )

        if message_type == "image":
            image = data['image']
            image_name = data['image_name']
            image_type = data['image_type']

            decoded_image = base64.b64decode(image)
            content_file = ContentFile(decoded_image, name=image_name)

            await self.save_message(user=user, image=content_file)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': 'image',
                    'image': image,
                    'image_type': image_type,
                    'user': user,
                    'name': name,
                    'created': datetime.now().strftime("%b. %d, %Y, %I:%M %p")
                }
            )

    async def chat_message(self, event):
        message_type = event['message_type']
        name = event['name']
        user = event['user']
        created = event['created']

        if message_type == "message":
            body = event['body']
            await self.send(text_data=json.dumps({
                'message_type': message_type,
                'body': body,
                'user': user,
                'name': name,
                'created': created,
            }))

        if message_type == "voice":
            voice = event['voice']
            await self.send(text_data=json.dumps({
                'message_type': message_type,
                'voice': voice,
                'user': user,
                'name': name,
                'created': created,
            }))

        if message_type == "image":
            image = event['image']
            image_type = event['image_type']
            await self.send(text_data=json.dumps({
                'message_type': message_type,
                'image': image,
                'image_type': image_type,
                'user': user,
                'name': name,
                'created': created,
            }))

    @sync_to_async
    def save_message(self, user, body=None, voice=None, image=None):
        useraccount = User.objects.get(id=user)
        myclass = Class.objects.get(id=self.class_id)
        ClassMessage.objects.create(user=useraccount, myclass=myclass, body=body, voice=voice, image=image)

    @sync_to_async
    def get_name(self, user):
        useraccount = User.objects.get(id=user)
        return useraccount.username
