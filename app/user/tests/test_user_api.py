"""
test user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user succeed"""
        payload = {
            "email": "test@example.com",
            "password": "Testpass123",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exist_error(self):
        """test return an error if user email exist"""

        payload = {
            "email": "test@example.com",
            "password": "Testpass123",
            "name": "Test Name",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """test an error is returned id password less than 8 chars"""
        payload = {"email": "test@example.com", "password": "Test", "name": "Test Name"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {
            "name": "test Name",
            "email": "test@example.com",
            "password": "test-user-pass123",
        }
        create_user(**user_details)
        payload = {"email": user_details["email"], "password": user_details["password"]}
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credentials invalid"""
        create_user(email="test@example.com", password="goodpass")
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting bad password return error"""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for the users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    class PrivateUserAPITests(TestCase):
        """Test API requess that requires authentication"""

        def setUp(self):
            self.user = create_user(
                email="test@example.com", password="testpass123", name="Test Name"
            )
            self.client = APIClient()
            self.client.force_authenticate(user=self.user)

        def test_retrieve_profile_success(self):
            """Test retrieving profiles for logged in user"""
            res = self.client.get(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(
                res.data,
                {
                    "name": self.user.name,
                    "email": self.user.email,
                },
            )

        def test_post_me_not_allowed(self):
            """test Post is not allowed for the me endpoint"""
            res = self.client.post(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_update_user_profile(self):
            """test updating user profile for the authenticated user"""
            payload = {"email": "test@example.com", "password": "newpassword123"}
            res = self.client.patch(ME_URL, payload)
            self.user.refresh_from_db()
            self.assertEqual(self.user.name, payload["name"])
            self.assertTrue(self.user.check_password(payload["password"]))
            self.assertEqual(res.status_code, status.HTTP_200_OK)
