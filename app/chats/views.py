import logging

from rest_framework import permissions, status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from chats.serializers import MessageSerializer
from core import models

logger = logging.getLogger(__name__)


class ChatView(APIView):
    """Chat api endpoint"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            other_username = self.request.query_params.get("other_username", None)
            if other_username is None:
                return Response(
                    "Please provide other_username query param",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            me = self.request.user
            other_user = models.User.objects.get(username=other_username)
            thread_obj = models.Thread.objects.get_or_create_personal_thread(
                me, other_user
            )
            messages = models.Message.objects.filter(thread=thread_obj.id)

            if not messages.exists():
                models.Message.objects.create(
                    sender=self.request.user,
                    text="This is the start of a new message",
                    thread=thread_obj,
                    is_bot=True
                )
            messages = models.Message.objects.filter(thread=thread_obj.id)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
