from rest_framework import viewsets, serializers, status
from products.models import Product
from .serializers import (
    ShoppingCartSerializer,
    OrderSerializer,
    CartItemSerializer,
    OrderItemSerializer,
)
from rest_framework.decorators import action
from .models import ShoppingCart, Order, CartItem, OrderItem
from core.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from core.permissions import IsAuthenticatedAndReadOnlyPermission
from rest_framework.authentication import TokenAuthentication

from django.db.models import FloatField
from django.db.models import F
from django.db.models import Sum


class ShoppingcartViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows carts to be viewed or edited.
    """

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    authentication_classes = [IsAuthenticatedAndReadOnlyPermission]
    permission_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        retrieve shoppingcart for authenticated user
        """
        user = self.request.user
        return self.queryset.filter(customer=user)

    @action(detail=True, methods=["post", "put"])
    def add_to_cart(self, request, pk=None):
        """
         Add an item to a user's cart.
        Adding to cart is disallowed if there is not enough inventory for the
        product available. If there is, the quantity is increased on an existing
        cart item or a new cart item is created with that quantity and added
        to the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.

        """
        cart = self.get_object()

        try:
            product = Product.objects.get(id=request.data["product_id"])
            quantity = int(request.data["quantity"])
        except Exception as e:
            print(e)
            return Response({"status": "fail"})

        # if product in stock - quantity asked < 0 or quantity available = 0
        if (
            product.inventory.get_available_quantity <= 0
            or product.inventory.get_available_quantity - quantity < 0
        ):
            # print that the product is not available
            print(_("There is no more product available"))
            return Response({"status": "fail"})

        existing_cart_product = CartItem.objects.filer(
            cart=cart, product=product
        ).first()

        # avant d'ajouter un produit,
        # regader s'il est pas deja present dans cart
        if existing_cart_product:
            existing_cart_product.quatity += quantity
            existing_cart_product.save()
        else:
            new_product = CartItem(
                cart=cart,
                product=product,
                quantity=quantity,
            )

            new_product.save()

        serializer = CartItemSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["patch", "delete"])
    def remove_from_cart(self, request, pk=None):
        """
        ustomers can only remove items from the
        cart 1 at a time, so the quantity of the product to remove from the cart
        will always be 1. If the quantity of the product to remove from the cart
        is 1, delete the cart item. If the quantity is more than 1, decrease
        the quantity of the cart item, but leave it in the cart.
        Parameters
        ----------
        :param request:
        :return: Updated cart
        """
        cart = self.get_object()

        try:
            product = Product.objects.get(id=request.data["product_id"])

        except Exception as e:
            print(e)
            return Response({"status": "fail"})

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
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
        serializer = CartItemSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    APi that allow cart items to be viewed or edited
    allow only admin user to modify shopping cart
    """

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = [IsAuthenticatedAndReadOnlyPermission]
    permission_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        retrieve cart item for authenticated users
        """
        user = self.request.user
        return self.queryset.filter(customer=user)


class OrderViewset(viewsets.ModelViewSet):
    """
    API endpoint to allow order to be viewed and created
    """

    # to place an order the user must be connected
    authentication_classes = [IsAuthenticatedAndReadOnlyPermission]
    permission_classes = [TokenAuthentication]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return self.queryset.filter(customer=user)

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
        serializer: Order Serialiazer
        Serialized representation of Order we are creating.
        """

        try:
            purchaser_id = self.request.data["customer"]
            user = User.objects.get(id=purchaser_id)
        except Exception:
            raise serializers.ValidationError(_("User was not found"))

        cart = user.cart

        for cart_item in cart.product.all():

            if cart_item.inventory.get_available_quatity - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    _("We do not have enough inventory of ")
                    + str(cart_item.product.name)
                    + _("to complete your purchase. Sorry, we will restock soon")
                )

        # find the order total using the quantity of each cart
        # item and the product's price
        total_aggregated_dict = cart.items.aggregate(
            total=Sum(F("quantity") * F("product__price"), output_field=FloatField())
        )

        order_total = round(total_aggregated_dict["total"], 2)
        order = serializer.save(customer=user, amount_due=order_total)

        order_items = []
        for cart_item in cart.product.all():
            order_items.append(
                OrderItem(
                    order=order, product=cart_item.product, quantity=cart_item.quantity
                )
            )
            # available_inventory should decrement by the appropriate amount
            cart_item.inventory.quantity_sold += cart_item.quantity
            cart_item.inventory.save()

        OrderItem.objects.bulk_create(order_items)
        # use clear instead of delete since it removes all objects from the
        # related object set. It does not delete the related objects it just
        # disassociates them, which is what we want in order to empty the cart
        # but keep cart items in the db for customer data analysis
        cart.items.clear()

    def create(self, request, *args, **kwargs):
        """
        Override the creation of Order objects.
        Parameters
        ----------
        request: dict
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, url_path="order_history/(?P<customer_id>[0-9])")
    def order_history(self, request, customer_id):
        """Return a list of a user's orders.
        Parameters
        ----------
        request: request
        """
        try:
            user = User.objects.get(id=customer_id)

        except Exception:
            # no user was found, so order history cannot be retrieved.
            return Response({"status": "fail"})

        orders = Order.objects.filter(customer=user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows order items to be viewed or edited.
    """

    authentication_classes = [IsAuthenticatedAndReadOnlyPermission]
    permission_classes = [TokenAuthentication]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return self.queryset.filter(customer=user)
