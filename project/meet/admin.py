from django.contrib import admin
from .models import User, Countries, Interests, Message, Activities, Events, Room, Liked

# Register your models here.
admin.site.register(User)
admin.site.register(Countries)
admin.site.register(Interests)
admin.site.register(Message)
admin.site.register(Activities)
admin.site.register(Events)
admin.site.register(Room)
admin.site.register(Liked)