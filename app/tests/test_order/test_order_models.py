from django.test import TestCase
from order.models import Order, ShoppingCart, OrderItem, CartItem
from order.factories import (
    OrderFactory,
    ShoppingCartFactory,
    OrderItemFactory,
    CartItemFactory,
)


class OrderModelTest(TestCase):
    def setUp(self) -> None:
        OrderItemFactory.create()
        OrderItemFactory.create()
        OrderFactory.create()
        OrderFactory.create()
        ShoppingCartFactory.create()
        ShoppingCartFactory.create()
        CartItemFactory.create()
        CartItemFactory.create()

    def test_create_order(self):
        order = Order.objects.all()
        self.assertTrue(len(order) > 1)

    def test_create_orderitem(self):
        orderitems = OrderItem.objects.all()
        self.assertTrue(len(orderitems) > 1)

    def test_create_shoppingart(self):
        cart = ShoppingCart.objects.all()
        self.assertTrue(len(cart) > 1)

    def test_create_cartitem(self):
        cartitems = CartItem.objects.all()
        self.assertTrue(len(cartitems) > 1)
