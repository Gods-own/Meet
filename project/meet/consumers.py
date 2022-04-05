import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message, User, Room, Notifications, Connected
from datetime import datetime
from django.db.models import Q, Count


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        #Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.seeroom()

        await self.connect_user()

        await self.accept()

    async def disconnect(self, close_code):
        
        #Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.seeroom()

        await self.disconnect_user()

    #Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        userid1 = data['user1']
        userid2 = data['user2']
        
        # await self.save_room(room, userid1, userid2)
        await self.save_message(userid2, username, room, message)

        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    #Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        no_of_connected_users = await self.get_connected_users()  
        checkuser = await self.checkuser(username)
        get_extra_info = await self.get_extra_info(username)
        get_notifications = await self.get_notifications()
        # Send message to websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'connected_users': no_of_connected_users,
            'checkuser': checkuser,
            'get_extra_info': get_extra_info,
            'get_notifications': get_notifications
        }))

    # @sync_to_async
    # def save_message(self, username, room, message):
    #     Message.objects.create(username=username, room=room, content=message)
    # @sync_to_async
    # def save_room(self, room, userid1, userid2):
    #     user1 = User.objects.get(pk=userid1)
    #     user2 = User.objects.get(pk=userid2)
    #     result1 = Room.objects.filter(Q(user1=user1) & Q(user2=user2)).exists()
    #     result2 = Room.objects.filter(Q(user1=user2) & Q(user2=user1)).exists()
    #     if result1 == False and result2 == False:
    #         Room.objects.create(room=room, user1=user1, user2=user2)    
    @database_sync_to_async
    def save_message(self, userid2, username, room, message):
        user2 = User.objects.get(pk=userid2)
        theroom = Room.objects.get(room=room)
        username = User.objects.get(username=username)
        chat = Message.objects.create(username=username, room=theroom, content=message)
        theroom.date_updated = datetime.now()
        theroom.save()
        notification = Notifications.objects.create(notification_user=user2, notification_message=chat)

    @database_sync_to_async
    def connect_user(self):
        connectedUser = User.objects.get(username=self.scope['user'])
        theroom = Room.objects.get(room=self.scope['url_route']['kwargs']['room_name'])
        if Connected.objects.filter(Q(connected_user=connectedUser) & Q(connection_room=theroom)).exists() == False:
            chat = Connected.objects.create(connected_user=connectedUser, connection_room=theroom, channel_name=self.channel_name)
        if Message.objects.filter(room=theroom).exists():    
            messagess = Message.objects.filter(room=theroom)
            notification = Notifications.objects.filter(notification_message__in=messagess)
            print(str(notification.last().notification_user.username) == str(self.scope['user']))
            print(self.scope['user'])
            print(notification.last().notification_user.username)
            if str(notification.last().notification_user.username) == str(self.scope['user']):
                print(notification)
                notification.update(notification_read=True)


    @database_sync_to_async
    def disconnect_user(self):
        connectedUser = User.objects.get(username=self.scope['user'])
        theroom = Room.objects.get(room=self.scope['url_route']['kwargs']['room_name'])
        if Connected.objects.filter(Q(connected_user=connectedUser) & Q(connection_room=theroom)).exists():
            Connected.objects.filter(Q(connected_user=connectedUser) & Q(connection_room=theroom)).delete()

    @database_sync_to_async
    def get_connected_users(self):
        theroom = Room.objects.get(room=self.scope['url_route']['kwargs']['room_name'])
        no_of_connected_users1 = Connected.objects.filter(connection_room=theroom).count()  
        return no_of_connected_users1 
         
    @sync_to_async
    def seeroom(self):
        print(self.room_name)    
        print (self.scope['user'])

    @sync_to_async
    def checkuser(self, username):
        if str(self.scope['user']) == username:
            return True
        else:
            return False 

    @database_sync_to_async
    def get_extra_info(self, username):
        theroom = Room.objects.get(room=self.scope['url_route']['kwargs']['room_name'])
        username = User.objects.get(username=username)
        messagess = Message.objects.filter(room=theroom, username=username).last()
        msgObj = {'userImage':messagess.username.userImage.url, 'date_added': messagess.date_added.strftime("%b %d, %Y, %I:%M %p")}
        return msgObj      

    @database_sync_to_async
    def get_notifications(self):
        username = User.objects.get(username=self.scope['user'])
        no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
        return no_of_notifications

    

    
