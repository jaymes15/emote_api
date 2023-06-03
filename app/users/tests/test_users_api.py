from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core.helpers import sample_user
from users.serializers import AllUserSerializer, UserUpdateSerializer

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token_obtain_pair")
REFRESH_TOKEN_URL = reverse("users:token_refresh")
ME_URL = reverse("users:me")
GET_ALL_USERS_URL = reverse("users:all_users-list")


def get_get_all_users_detail_url(id):
    return reverse("users:all_users-detail", args=[id])


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.username = "test_user"
        self.password = "testpass001"

    def test_create_valid_user_success(self):
        """Test creating using with a valid payload is successful"""

        payload = {
            "username": self.username,
            "password": self.password,
            "first_name": "John",
            "last_name": "Doe",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.last()
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            "username": self.username,
            "password": self.password,
            "first_name": "John",
            "last_name": "Doe",
        }

        sample_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password with length less than 8 fails"""
        payload = {"username": self.username, "password": "pw"}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(username=payload["username"]).exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        credentials = {"username": self.username, "password": self.password}

        sample_user(**credentials)

        res = self.client.post(TOKEN_URL, credentials)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", res.data)
        self.assertIn("access", res.data)

    def test_refresh_token(self):
        """Test refresh token"""
        # Get user token
        credentials = {"username": self.username, "password": self.password}

        sample_user(**credentials)

        res = self.client.post(TOKEN_URL, credentials)

        # refresh token
        payload = {"refresh": res.data["refresh"]}
        res = self.client.post(REFRESH_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        user = sample_user(username=self.username, password=self.password)
        payload = {"username": user.username, "password": "wrong"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_is_not_created_if_user_does_not_exist(self):
        """Test that token is not created if user doens't exist"""
        payload = {"username": self.username, "password": self.password}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_field(self):
        """Test that username and password are required"""
        res = self.client.post(TOKEN_URL, {"username": "one", "password": ""})

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.password = "testpass"
        self.username = "testuser"
        self.user = sample_user(
            username=self.username,
            password=self.password,
            first_name="John",
            last_name="Doe",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        serializer = UserUpdateSerializer(self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            "first_name": "Julia",
            "last_name": "Roberts",
            "password": "newpassword123",
            "current_password": self.password,
        }

        res = self.client.put(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_partial_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {"last_name": "Roberts"}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, payload["last_name"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_not_update_username(self):
        """Test user can update their username"""
        payload = {"username": "JohnJoe12"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertNotEqual(self.user.username, payload["username"])
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestAllUserViewset(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_1 = sample_user()
        self.user_2 = sample_user(username="another_user")
        self.normal_user = sample_user(username="normal_user")

    def test_user_can_get_all_users(
        self,
    ) -> None:
        """Test user can GET all users"""

        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(GET_ALL_USERS_URL)
        all_users = models.User.objects.all().exclude(id=self.user_1.id)
        serializer = AllUserSerializer(all_users, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(all_users.count(), 2)

    def test_retrieve(
        self,
    ) -> None:
        """Test a user can GET one single user"""

        self.client.force_authenticate(user=self.user_1)

        url = get_get_all_users_detail_url(id=self.user_2.id)
        response = self.client.get(url)
        serializer = AllUserSerializer(self.user_2, many=False)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_post_not_allowed(
        self,
    ) -> None:
        """Test POST method not allowed"""

        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(GET_ALL_USERS_URL)

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_not_allowed(
        self,
    ) -> None:
        """Test UPDATE, PATCH method not allowed"""

        self.client.force_authenticate(user=self.user_1)

        url = get_get_all_users_detail_url(id=self.user_1.id)
        response = self.client.patch(url)

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(
        self,
    ) -> None:
        """Test DELETE method not allowed"""

        self.client.force_authenticate(user=self.user_1)

        url = get_get_all_users_detail_url(id=self.user_1.id)
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
