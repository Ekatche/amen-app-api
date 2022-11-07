from django.test import TestCase
from order.models import Order, ShoppingCart
from order.factories import OrderFactory, ShoppingCartFactory


class OrderModelTest(TestCase):
    def setUp(self) -> None:
        OrderFactory.create()
        OrderFactory.create()
        ShoppingCartFactory.create()
        ShoppingCartFactory.create()

    def test_create_order(self):
        order = Order.objects.all()
        self.assertTrue(len(order)>1)

    def test_create_shoppingart(self):
        cart = ShoppingCart.objects.all()
        self.assertTrue(len(cart)>1)

