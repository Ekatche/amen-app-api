import random
from django.core.management.base import BaseCommand

# from django.db import transaction
from django.db.utils import IntegrityError

# import models
from products.models import Product, Media, Promotion, Coupons
from inventory.models import Inventory
from categories.models import Category, SubCategory
from order.models import Order, ShoppingCart, OrderItem, CartItem
from core.models import User, ShippingAddress, BillingAddress

# Import factories

from core.factories import UserFactory, BillingAddressFactory, ShippingAddressFactory
from order.factories import (
    OrderFactory,
    ShoppingCartFactory,
    OrderItemFactory,
    CartItemFactory,
)
from products.factories import (
    ProductFactory,
    PromotionFactory,
    MediaFactory,
    CouponsFactory,
)
from categories.factories import CategoryFactory, SubCategoryFactory
from inventory.factories import InventoryFactory

NUM_USERS = 50
NUM_PROMO = 6
NUM_PRODUCT = 50
NUM_ORDER = 60
NUM_CART = 30
NUM_CAT = 4
NUM_SUBCAT = 7


class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        models = [
            Media,
            Product,
            Promotion,
            Category,
            SubCategory,
            Coupons,
            Inventory,
            OrderItem,
            Order,
            ShoppingCart,
            CartItem,
            ShippingAddress,
            BillingAddress,
            User,
        ]
        for model in models:
            if str(model) != "<class 'core.models.User'>":
                model.objects.all().delete()
                self.stdout.write(str(model))
            else:
                model.objects.exclude(email="amen@amen.com").delete()

        self.stdout.write("Creating new data ...")
        people = []
        products = []

        self.stdout.write("Creating users  ...")

        for _ in range(NUM_USERS):
            person = UserFactory()
            ShippingAddressFactory(customer=person)
            BillingAddressFactory(customer=person)
            people.append(person)

        self.stdout.write("Creating Products ...")

        for _ in range(NUM_CAT):
            cat = CategoryFactory()
            subcategory = SubCategoryFactory(category=cat)
            for _ in range(NUM_PRODUCT):
                product = ProductFactory(subcategory=subcategory, categories=(cat,))
                InventoryFactory(product=product)
                MediaFactory(product=product)
                products.append(product)

        self.stdout.write("Creating Promotion and coupons  ...")

        for _ in range(NUM_PROMO):
            coupons = CouponsFactory()
            PromotionFactory(coupons=coupons)

        self.stdout.write("Creating cart and adding product in ...")
        for _ in range(NUM_CART):
            unique = False
            while not unique:
                try:
                    customer = random.choice(people)
                    cart = ShoppingCartFactory(customer=customer)
                    products_com = random.choices(products, k=8)
                    for prod in products_com:
                        CartItemFactory(cart=cart, product=prod)
                    unique = True
                except IntegrityError:
                    pass

        self.stdout.write("Creating Order ...")
        for _ in range(NUM_ORDER):
            unique = False
            while not unique:
                try:
                    customer = random.choice(people)
                    order = OrderFactory(
                        customer=customer, shipping=customer.shippingaddress.get()
                    )

                    products_com = random.choices(products, k=8)
                    for prod in products_com:
                        OrderItemFactory(order=order, product=prod)
                    unique = True
                except IntegrityError:
                    pass

        self.stdout.write("Finish creating new data ...")
