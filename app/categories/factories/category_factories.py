import factory
from ..models import Category, SubCategory
import random
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import BaseProvider


class CategoryProvider(BaseProvider):
    def category(self):
        category = ["Makeup", "SkinCare", "HairCare", "Perfume"]
        return random.choice(category)

    def subcategory(self):
        subcategory = ["Men", "Woman ", "Kid", "Shampoo"]
        return random.choice(subcategory)


fake = Faker()
fake.add_provider(CategoryProvider)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "cat_slug_%s" % n)

    slug = factory.Faker("slug")
    is_active = True


class SubCategoryFactory(DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = factory.Sequence(lambda n: "subcat_slug_%s" % n)
    category = factory.SubFactory(CategoryFactory)
