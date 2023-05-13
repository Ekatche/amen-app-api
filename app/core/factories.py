import factory
from .models import User, BillingAddress, ShippingAddress
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers.person.fr_FR import Provider as Person
from faker.providers.address.fr_FR import Provider as Address

fake = Faker()
fake.add_provider(Person)
fake.add_provider(Address)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda u: f"{u.first_name}.{u.last_name}@test.com")


class UserAdminFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = fake.first_name()
    last_name = fake.last_name()
    amen_role = "amen_admin"


class BillingAddressFactory(DjangoModelFactory):
    class Meta:
        model = BillingAddress

    building_number = fake.building_number()
    street = factory.Faker("street_name")
    city = factory.Faker("city")
    postcode = factory.Faker("postcode")
    customer = factory.SubFactory(UserFactory)
    country = "France"


class ShippingAddressFactory(DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    building_number = fake.building_number()
    street = factory.Faker("street_name")
    city = factory.Faker("city")
    postcode = factory.Faker("postcode")
    customer = factory.SubFactory(UserFactory)
    country = "France"
