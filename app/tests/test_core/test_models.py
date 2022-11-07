"""
test for models_legacy
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import BillingAddress, ShippingAddress
from core.factories import BillingAddressFactory, ShippingAddressFactory, UserFactory


class ModelTests(TestCase):
    """Test models_legacy"""

    def setUp(self):
        user = UserFactory(email="texto@text.com", first_name="tyty", last_name="Test")
        BillingAddressFactory.create(customer=user)
        ShippingAddressFactory.create()

    def test_create_user_with_email_successful(self):
        email = "testo@example.com"
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

    def test_create_billing_address(self):
        billingAddress = BillingAddress.objects.get()
        self.assertEqual(billingAddress.address, "12 Rue des tests 38300 Tests City")

    def test_creating_shipping_address(self):
        shippingAddress = ShippingAddress.objects.get()
        self.assertEqual(shippingAddress.address, "12 Rue des tests 38300 Tests City")
