import factory

from ..models import Category, SubCategory

from factory.django import DjangoModelFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = "Sample Category name"
    slug = factory.Faker("slug")
    is_active = True


class SubCategoryFactory(DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = "Sample SubCategory name"
    category = factory.SubFactory(CategoryFactory)
