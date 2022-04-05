from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import time

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField()
    dateofbirth = models.DateField(null=True)
    introduction = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=100)
    userImage = models.ImageField(upload_to="userimg/%y", default="userimg/21/default-Image.png")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "age": self.age,
            "dateofbirth": self.dateofbirth,
            "introduction": self.introduction,
            "gender": self.gender,
            "userImage": self.userImage.url
        }


class Interests(models.Model):
    hobbies = models.CharField(max_length=100, unique=True)
    user_hobby = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="hobbysist")
    def __str__(self):
        return f"{self.user_hobby}"

class Countries(models.Model):
    country = models.CharField(max_length=100, unique=True, default=None)
    user_country = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="citizen")
    def __str__(self):
        return f"{self.user_country}"


class Activities(models.Model):
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poster")
    activity = models.TextField()
    picture = models.ImageField(upload_to="img/%y")
    hobby = models.ForeignKey(Interests, on_delete=models.CASCADE, default=None, related_name="post_hobby")
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "posterImage": self.poster.userImage.url,
            "activity": self.activity,
            "picture": self.picture.url,
            "hobby": self.hobby.hobbies,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d, %Y, %I:%M %p")
        }

    @property
    def picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture_url

class Liked(models.Model):
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_liker")
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name="post")
    is_liked = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "liker": self.liker.username,
            "activity": self.activity.activity,
            "is_liked": self.is_liked
        }

class Events(models.Model):
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=500, default="Message poster for more details")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listed_by")
    description = models.TextField()
    hobby_events = models.ForeignKey(Interests, on_delete=models.CASCADE, related_name="hobby_acuvity")
    event_location = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name="eventLocation")
    event_date = models.DateField(auto_now=False)
    event_time = models.TimeField(auto_now=False, null=True)
    is_closed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

class Room(models.Model):
    room = models.CharField(max_length=255)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chatter1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chatter2")
    date_updated = models.DateTimeField(null=True)


class Message(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="dm_room")
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "userImage": self.username.userImage.url,
    #         "date_added": self.date_added.strftime("%b %d, %Y, %I:%M %p"),
    #     }

# class Message(models.Model):
#     username = models.CharField(max_length=255)
#     room = models.CharField(max_length=255)
#     content = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('date_added',)

class Notifications(models.Model):
    notification_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_to")
    notification_message =  models.ForeignKey(Message, on_delete=models.CASCADE, related_name="new_message")
    notification_read = models.BooleanField(default=False)

class Connected(models.Model):
    connected_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="connected_user")
    connection_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="connected_room")
    channel_name = models.TextField()   
    connect_date = models.DateTimeField(auto_now_add=True)