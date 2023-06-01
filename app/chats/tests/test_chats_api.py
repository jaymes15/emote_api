from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chats.serializers import MessageSerializer
from core import models
from core.helpers import sample_user
from core.tests import utils

CHATS_URL = reverse("chats:chats")


class TestChatView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_1 = sample_user()
        self.user_2 = sample_user(username="another_user")

        self.message = utils.sample_create_message(
            user_1=self.user_1, user_2=self.user_2
        )

    def test_get_all_messages_between_user_1_and_user_2(
        self,
    ) -> None:
        """Test GET all message between user_1 and user_2"""

        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(CHATS_URL, {"other_username": self.user_2.username})
        messages = models.Message.objects.filter(thread=self.message.thread)
        serializer = MessageSerializer(messages, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)
