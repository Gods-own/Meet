
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("message/<int:userid2>/<str:room_name>/", views.room, name="room"),
    path("create", views.create_activity, name="createActivity"),
    path("edit/<int:activity_id>", views.edit_activity, name="editActivity"),
    path("createEvent", views.create_event, name="createEvent"),
    path("events", views.event, name="event"),
    path("profile/<int:user_id>", views.profile, name="person"),
    path("search", views.search, name="search"),
    path("post/<int:activity_id>", views.view_post, name="viewPost"),
    path("messages/", views.messages, name="messages"),
    path("addInterests/<int:user_id>", views.add_interests, name="addInterests"),
    path("settings", views.editProfile, name="settings"),

    path("like/<int:activity_id>", views.like_post, name="like"),
    path("isliked/<int:activity_id>", views.isliked, name="isliked"),
    path("notification/<int:userid2>", views.notification, name="notification"),
    path("sidesearch", views.sidesearch, name="sidesearch"),
]