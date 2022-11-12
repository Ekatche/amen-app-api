import factory
from ..models import Order, ShoppingCart, CartItem, OrderItem
from factory.django import DjangoModelFactory
from products.factories import ProductFactory
from core.factories import UserFactory, ShippingAddressFactory


class ShoppingCartFactory(DjangoModelFactory):
    class Meta:
        model = ShoppingCart

    customer = factory.SubFactory(
        UserFactory,
    )


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    product = factory.SubFactory(
        ProductFactory,
    )
    quantity = factory.Faker("pyint", min_value=1, max_value=5)

    cart = factory.SubFactory(
        ShoppingCartFactory,
    )


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(
        UserFactory,
    )
    shipping = factory.SubFactory(ShippingAddressFactory)
    amount_due = factory.Faker("pyint", min_value=5, max_value=100)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = factory.Faker("pyint", min_value=1, max_value=5)
