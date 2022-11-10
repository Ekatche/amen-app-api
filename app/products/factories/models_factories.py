import factory
from decimal import Decimal
from factory.django import DjangoModelFactory
from inventory.factories import InventoryFactory
from ..models import Promotion, Product, Coupons, Media


# defining factories


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = "Sample recipe name"
    is_available = True
    on_promo = False
    price = Decimal("5.50")
    description = "Sample receipe description."
    inventory = factory.SubFactory(InventoryFactory)


class CouponsFactory(DjangoModelFactory):
    class Meta:
        model = Coupons

    name = "TRENTEPOURCENTS"
    code = "MOINS30"
    discount = 30
    is_active = True


class PromotionFactory(DjangoModelFactory):
    class Meta:
        model = Promotion

    name = "OCTOBERTEST22"
    period = 2
    coupons = factory.SubFactory(CouponsFactory)


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = Media

    product = factory.SubFactory(ProductFactory)
    image = "image/default.png"


class ProductWithPromoFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = "Sample discoup product name"
    is_available = True
    on_promo = True
    price = Decimal("5.50")
    description = "Sample descounted product description."
    promo = factory.SubFactory(PromotionFactory)
