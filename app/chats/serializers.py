import datetime

from django.conf import settings
from rest_framework import serializers

from core.models import Message
from users.serializers import AllUserSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Message model serializer"""

    sender = AllUserSerializer(read_only=True, many=False)

    class Meta(object):
        model = Message
        fields = (
            "id",
            "thread",
            "sender",
            "text",
            "created_at",
            "updated_at",
            "is_bot"
        )
        read_only_fields = (
            "id",
            "thread",
            "sender",
            "text",
            "created_at",
            "updated_at",
            "is_bot"
        )
