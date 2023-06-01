import logging
import os
import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


def image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join(os.environ.get("IMAGE_PATH"), filename)


class UserManager(BaseUserManager):
    """Custom User model manager"""

    def create_user(self, username, password=None, **extra_fields):
        """Create and saves a new user"""
        FUNCTION_NAME: str = "UserManager.create_user"
        logger.info(f"function:{FUNCTION_NAME}   Message: Creating user")
        if not username:
            logger.error(
                f"function:{FUNCTION_NAME}   Message: Users must have a username"
            )
            raise ValueError("Users must have a username")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.created_on = timezone.now()

        user.save(using=self._db)

        logger.info(
            f"function:{FUNCTION_NAME}   Message: User {username} has been created"
        )

        return user

    def create_superuser(self, username, password):
        """Creates and saves a new super user"""
        FUNCTION_NAME: str = "UserManager.create_superuser"
        logger.info(f"function:{FUNCTION_NAME}   Message: Creating super user")

        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        logger.info(
            f"function:{FUNCTION_NAME}   Message: super user {username} has been created"
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    username = models.CharField(max_length=255, unique=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=image_file_path, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)
