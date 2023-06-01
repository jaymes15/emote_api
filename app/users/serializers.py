import django.contrib.auth.password_validation as validators
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import User
from users.utils.whitelist import is_list_allowed


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "profile_picture",
            "username",
            "created_on",
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = (
            "password",
            "first_name",
            "last_name",
            "profile_picture",
            "username",
            "created_on",
        )

        extra_kwargs = {
            "password": {"write_only": True, "min_length": settings.PASSWORD_LENGTH}
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return super().update(instance, validated_data)

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get("password")

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(
            required=False,
        )
        self.fields["password"] = serializers.CharField(
            required=False,
            style={"input_type": "password"},
            trim_whitespace=False,
            write_only=True,
        )

    def validate(self, attrs):
        # implement your logic here
        try:
            user_query = get_user_model().objects.filter(username=attrs["username"])

            if user_query.exists():
                if user_query.last().is_active:
                    attrs["username"] = user_query.last().username
                    data = super().validate(attrs)
                    return data
                else:
                    raise exceptions.AuthenticationFailed(
                        "This account is not active",
                        "inactive_account",
                    )

            else:
                raise exceptions.AuthenticationFailed(
                    "Account not found",
                    "account_not_found",
                )
        except Exception:
            raise exceptions.AuthenticationFailed(
                "Account not found",
                "account_not_found",
            )


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    current_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "password",
            "current_password",
            "first_name",
            "last_name",
            "profile_picture",
            "username",
            "created_on",
        )
        read_only_fields = ("id", "username", "created_on")
        extra_kwargs = {
            "password": {
                "required": False,
                "write_only": True,
                "min_length": settings.PASSWORD_LENGTH,
            },
        }

    def get_password_white_list(self):
        return [
            "first_name",
            "last_name",
            "profile_picture",
        ]

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        validated_data.pop("current_password", None)

        if password:
            instance.set_password(password)
            instance.save()

        return super().update(instance, validated_data)

    def _isValidPassword(self, password):
        return self.context.get("request").user.check_password(password)

    def validate(self, attrs):
        """Validate and authenticate the user"""

        if not is_list_allowed(list(attrs), self.get_password_white_list()):

            password = attrs.get("current_password")

            if not password or not self._isValidPassword(password):
                msg = _(f"Incorrect password")
                raise serializers.ValidationError(msg, code="authorization")

        return attrs
