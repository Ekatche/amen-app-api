from ..models import Category

from factory.django import DjangoModelFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = "Sample recipe name"
    slug = "test slug"
    is_active = True
