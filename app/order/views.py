from rest_framework import viewsets
from rest_framework import serializers
from products.models import Product
from .serializers import ShoppingCartSerializer, OrderSerializer
from rest_framework.decorators import action
from order.models import ShoppingCart, Order
from core.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import FloatField
from django.db.models import F
from django.db.models import Sum


# Updat this view


class ShoppongcartViewset(viewsets.ModelViewSet):
    """
    API endpoint to allow users to add,
    retrieve products from shopping card
    """

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    @action(detail=True, methods=["post", "put"])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            product = Product.objects.get(id=request.data["product_id"])
            quantity = int(request.data["quantity"])
        except Exception as e:
            print(e)
            return Response({"status": "fail"})

        # si produit en stock - quantité <0 ou que quantité disponible = 0
        # print le produit n'est plus disponible

        existing_cart_product = ShoppingCart.objects.filer(
            cart=cart, product=product
        ).first()
        # avant d'ajouter un produit, regader s'il est pas deja present dans cart
        if existing_cart_product:
            existing_cart_product.quatity += quantity
            existing_cart_product.save()
        else:
            new_product = ShoppingCart(cart=cart, product=product, quantity=quantity)
            new_product.save()

        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["post", "put"])
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()

        try:
            product = Product.objects.get(pk=request.data["product_id"])

        except Exception as e:
            print(e)
            return Response({"status": "fail"})

        try:
            cart_item = ShoppingCart.objects.get(cart=cart, product=product)
        except Exception as e:
            print(e)
            return Response({"status": "fail"})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        # return the updated cart to indicate success
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)


class OrderViewset(viewsets.ModelViewSet):
    """
    API endpoint to allow order to be viewed and created
    """

    # to place an order the user must be connected
    authentication_classes = [IsAuthenticated]
    permission_classes = [TokenAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create_order(self, serializer):
        """
        Add info and perform checks before saving an Order.
        Before creating an Order, there is a check on the customer's cart items.
        If the cart item quantity causes the product's available inventory to
        dip below zero, a validation error is raised.If there is enough
        inventory to support the order, an Order is created
        and cart items are used to make order items. After that the cart is
        cleared.
        NOTE: Cart items are not deleted. When the cart is cleared the cart items
        still exist but are disassociated from the cart. The cart is empty so
        that the user can add new things to it, but cart items are preserved as
        they could be helpful in drawing insights from customer behavior or making
        suggestions. For example, what they have put in their cart previously,
        what other similar products might she/he like, etc.
        Parameters
        ----------
        serializer: OrderSerialiazer
        Serialized representation of Order we are creating.
        """

        try:
            purchaser_id = self.request.data["customer"]
            user = User.objects.get(pk=purchaser_id)
        except Exception:
            raise serializers.ValidationError("User was not found")

        cart = user.shoppingcart

        for cart_item in cart.product.all():

            if cart_item.inventory.total - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    "We do not have enough inventory of "
                    + str(cart_item.product.title)
                    + "to complete your purchase. Sorry, we will restock soon"
                )

        # find the order total using the quantity of each cart
        # item and the product's price
        total_aggregated_dict = cart.items.aggregate(
            total=Sum(F("quantity") * F("product__price"), output_field=FloatField())
        )

        order_total = round(total_aggregated_dict["total"], 2)
        order = serializer.save(customer=user, total=order_total)

        order_items = []
        for cart_item in cart.product.all():
            order_items.append(
                Order(
                    order=order, product=cart_item.product, quantity=cart_item.quantity
                )
            )
            # available_inventory should decrement by the appropriate amount
            cart_item.inventory.quantity_sold += cart_item.quantity
            cart_item.inventory.save()

        Order.objects.bulk_create(order_items)
        # use clear instead of delete since it removes all objects from the
        # related object set. It doesnot delete the related objects it just
        # disassociates them, which is what we want in order to empty the cart
        # but keep cart items in the db for customer data analysis
        cart.items.clear()
