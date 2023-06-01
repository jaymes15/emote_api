from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from core.models import User


def parse_bearer_token(headers):
    for key, value in headers:
        if key == b"authorization":
            auth_header = value.decode("utf-8")
            token_start_index = auth_header.index("Bearer ") + len("Bearer ")
            return auth_header[token_start_index:]


class TokenAuthMiddleware:
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        token = parse_bearer_token(scope["headers"])
        if not token:
            query_param = scope.get("query_string")
            byte_str = query_param.decode("utf-8")
            token = byte_str.split("=")[-1]

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            print(e)
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_data)
            user = await self.get_user(id=decoded_data["user_id"])

        scope["user"] = user
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, id):
        return User.objects.get(id=id)
