from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer
from products.models import Product, Promotion, Media
from categories.models import Category
from inventory.models import Inventory


html_strip = analyzer(
    "html_strip",
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"],
)


@registry.register_document
class ProductDocument(Document):
    inventory = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "quantity_sold": fields.IntegerField(),
            "total": fields.IntegerField(),
            "available_quantity": fields.IntegerField(attr="get_available_quatity"),
        },
        attr="inventory",
    )

    categories = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "slug": fields.TextField(),
            "is_active": fields.BooleanField(),
        },
        attr="categories",
        multi=True,
    )

    subcategory = fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "category": fields.ObjectField(
                properties={
                    "id": fields.IntegerField(),
                    "name": fields.TextField(),
                    "slug": fields.TextField(),
                    "is_active": fields.BooleanField(),
                }
            ),
        }
    )
    promo = fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "period": fields.IntegerField(),
            "coupons": fields.ObjectField(
                properties={
                    "id": fields.IntegerField(),
                    "name": fields.TextField(),
                    "code": fields.TextField(),
                    "discount": fields.IntegerField(),
                    "is_active": fields.BooleanField(),
                }
            ),
            "date_start": fields.DateField(),
            "date_end": fields.DateField(),
        }
    )
    images = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "image": fields.FileField(),
            "is_feature": fields.BooleanField(),
        },
        attr="images",
        multi=True,
    )

    class Index:
        # Name of the Elasticsearch index
        name = "product"

    class Django:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "slug",
            "description",
            "is_available",
            "on_promo",
            "promo_price",
        ]
        related_models = [Category, Inventory, Media, Promotion]

    def get_instances_from_related(self, related_instance):
        """
        If related_models is set, define how to retrieve the product instance(s)
        from the related model. The related_models option should be used with
        caution because it can lead in the index to the updating of a lot of items.
        """
        if isinstance(related_instance, Category):
            return related_instance.product.all()
        elif isinstance(related_instance, Inventory):
            return related_instance.product
        elif isinstance(related_instance, Media):
            return related_instance.product
        elif isinstance(related_instance, Promotion):
            return related_instance.product.all()
