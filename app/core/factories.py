import factory
from .models import User, BillingAddress, ShippingAddress
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    first_name = "Case"
    last_name = "Test"


class BillingAddressFactory(DjangoModelFactory):
    class Meta:
        model = BillingAddress

    building_number = "12"
    street = "Rue des tests"
    city = "Tests City"
    postcode = "38300"
    customer = factory.SubFactory(UserFactory)


class ShippingAddressFactory(DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    building_number = "12"
    street = "Rue des tests"
    city = "Tests City"
    postcode = "38300"
    customer = factory.SubFactory(UserFactory)
