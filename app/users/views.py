from django.core.exceptions import ValidationError
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import User
from users.serializers import (AllUserSerializer, LoginSerializer,
                               UserSerializer, UserUpdateSerializer)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        except ValidationError as err:
            return Response(data=err, status=status.HTTP_400_BAD_REQUEST)


class AllUserViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """Get All Users endpoint"""

    serializer_class = AllUserSerializer
    queryset = User.objects.all()

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)
