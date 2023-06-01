from os import environ
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from core import models


class ImageFilePathTest(TestCase):
    @patch("uuid.uuid4")
    def test_file_name_uuid(self, mock_uuid):
        """Test that image is save in the correct location"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid

        file_path = models.image_file_path(None, "myimage.jpg")

        expected_path = f"{environ.get('IMAGE_PATH')}{uuid}.jpg"
        self.assertEquals(file_path, expected_path)


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.username = "test_user"
        self.password = "test12345."

    def test_create_user_with_username_successful(self):
        """Test creating a new user with an username is successful"""

        user = get_user_model().objects.create_user(
            username=self.username, password=self.password
        )

        self.assertEqual(user.username, self.username)
        self.assertTrue(user.check_password(self.password))

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(self.username, self.password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_username_unique(self):
        """Test username is unique"""

        get_user_model().objects.create_user(
            password=self.password, username=self.username
        )

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                password=self.password,
                username=self.username,
            )
