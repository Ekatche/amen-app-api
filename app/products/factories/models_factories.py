import factory
from factory.django import DjangoModelFactory
from faker import Faker
from factory import fuzzy
from categories.factories import SubCategoryFactory
from ..models import Promotion, Product, Coupons, Media

# defining factories
fake = Faker()


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    slug = factory.Faker("slug")
    name = fuzzy.FuzzyText(length=12, prefix="PRODUCT_")
    is_available = True
    on_promo = False
    price = factory.Faker("pyint", min_value=5, max_value=100)
    description = fake.text()
    subcategory = factory.SubFactory(SubCategoryFactory)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of category were passed in, use them
            for category in extracted:
                self.category.add(category)


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = Media

    image = "image/default.png"
    product = factory.SubFactory(ProductFactory)


class CouponsFactory(DjangoModelFactory):
    class Meta:
        model = Coupons

    name = fuzzy.FuzzyText(length=12, prefix="COUPON_")

    code = fuzzy.FuzzyText(length=10, prefix="CODE_")
    discount = factory.Faker("pyint", min_value=10, max_value=50)
    is_active = True


class PromotionFactory(DjangoModelFactory):
    class Meta:
        model = Promotion

    name = fuzzy.FuzzyText(length=12, prefix="PROMO")
    period = factory.Faker("pyint", min_value=2, max_value=5)
    coupons = factory.SubFactory(CouponsFactory)


class ProductWithPromoFactory(DjangoModelFactory):
    class Meta:
        model = Product

    slug = fake.lexify(text="prod_slug_??????")
    name = fake.lexify(text="prod_name_??????")
    is_available = True
    on_promo = True
    price = factory.Faker("pyint", min_value=5, max_value=100)
    description = fake.text()
    promo = factory.SubFactory(PromotionFactory)
