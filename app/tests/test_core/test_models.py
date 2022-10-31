"""
test for models_legacy
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models_legacy"""

    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "test"
        first_name = "test"
        last_name = "Name"
        user = get_user_model().objects.create_user(
            email=email, password=password, first_name=last_name, last_name=first_name
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """test email is normalised"""
        sample_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """test that creating user without an email raises a valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "Test123")

    def test_create_super_user(self):
        """test creating superuser"""
        user = get_user_model().objects.create_superuser("tes@example.com", "test123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
