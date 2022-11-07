import factory
from ..models import Order, ShoppingCart
from factory.django import DjangoModelFactory
from products.factories import ProductFactory
from core.factories import UserFactory, ShippingAddressFactory


class ShoppingCartFactory(DjangoModelFactory):
    class Meta:
        model = ShoppingCart

    products = factory.SubFactory(
        ProductFactory,
    )

    customer = factory.SubFactory(
        UserFactory,
    )

    quantity = 2
    amount_due = 10


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    products = factory.SubFactory(
        ProductFactory,
    )

    customer = factory.SubFactory(
        UserFactory,
    )

    shipping = factory.SubFactory(ShippingAddressFactory)

    shoppingcart = factory.SubFactory(ShoppingCartFactory)
    quantity = 2

    amount_due = 10
