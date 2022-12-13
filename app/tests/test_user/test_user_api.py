"""
test user api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

login_url = reverse("user:login")
logout_url = reverse("user:logout")
signup_url = reverse("user:signup")
me_url = '/api/user/user/'
changePassWord_url = "/api/user/userChangePassword/"


# TOKEN_URL = reverse("create-user:token")
# ME_URL = reverse("user:me")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_signup_user_success(self):
        """Test creating a user succeed"""
        payload = {
            "email": "user@example.com",
            "phone_prefix": "+33",
            "phone_number": "00",
            "gender": "m",
            "password": "Testpass123",
            "password2": "Testpass123",
            "first_name": "test",
            "last_name": "case",
            "birth_date": "2022-12-13T13:24:51.977Z"
        }
        res = self.client.post(signup_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exist_error(self):
        """test return an error if user email exist"""

        payload = {
            "email": "user@example.com",
            "phone_prefix": "+33",
            "phone_number": "00",
            "gender": "m",
            "password": "Testpass123",
            "password2": "Testpass123",
            "first_name": "test",
            "last_name": "case",
            "birth_date": "2022-12-13T13:24:51.977Z"
        }
        create_user(**payload)

        res = self.client.post(signup_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """test an error is returned id password less than 8 chars"""
        payload = {
            "email": "user@example.com",
            "phone_prefix": "+33",
            "phone_number": "00",
            "gender": "m",
            "password": "tes",
            "password2": "tes",
            "first_name": "test",
            "last_name": "case",
            "birth_date": "2022-12-13T13:24:51.977Z"
        }
        res = self.client.post(signup_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exist)

    def test_password_mustmatch_error(self):
        """test an error is returned id password less than 8 chars"""
        payload = {
            "email": "user@example.com",
            "phone_prefix": "+33",
            "phone_number": "00",
            "gender": "m",
            "password": "test",
            "password2": "test12",
            "first_name": "test",
            "last_name": "case",
            "birth_date": "2022-12-13T13:24:51.977Z"
        }
        res = self.client.post(signup_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exist)

    def test_create_login_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
            "password": "test-user-pass123",
        }
        create_user(**user_details)
        payload = {"email": user_details["email"], "password": user_details["password"]}
        res = self.client.post(login_url, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_login_bad_credentials(self):
        """Test return error if credentials invalid"""
        create_user(
            email="test@example.com",
            password="goodpass",
            first_name="test",
            last_name="Name",
        )
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(login_url, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test posting bad password return error"""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(login_url, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for the users."""
        res = self.client.get(me_url + "3312/")

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requess that requires authentication"""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="Name",
        )
        user_details = {
            "first_name": "Taste",
            "last_name": "Name",
            "email": "testy@example.com",
            "password": "test-user-pass123",
        }
        self.user2 = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profiles for logged in user"""
        res = self.client.get(me_url + str(self.user.id) + "/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_me_not_allowed(self):
        """test Post is not allowed for the "me" endpoint"""
        res = self.client.post(me_url + str(self.user.id) + "/")

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating user profile for the authenticated user"""
        payload = {
            "email": "test@example.com",
            "first_name": "NAME",
        }
        res = self.client.patch(me_url + str(self.user.id) + "/", payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_password(self):
        """test updating user profile for the authenticated user"""
        payload = {
            "old_password": "testpass123",
            "new_password": "NEwpassPoert123",
        }
        res = self.client.patch(changePassWord_url, payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["new_password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def _login(self):
        data = {"email": "testy@example.com",
                "password": "test-user-pass123"}
        self.client.force_authenticate(user=self.user2)
        r = self.client.post(login_url, data)
        body = r.json()
        if 'access' in body["token"]:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['token']['access'])
        return r.status_code, body

    def test_logout_sucessfully(self):
        """ test if logout end point works"""
        _, body = self._login()
        r = self.client.post(logout_url)

        self.assertEquals(r.status_code, status.HTTP_200_OK)

