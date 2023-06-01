from django.urls import path

from chats import views
from chats.apps import ChatsConfig

app_name = ChatsConfig.name


urlpatterns = [
    path("", views.ChatView.as_view(), name="chats"),
]
