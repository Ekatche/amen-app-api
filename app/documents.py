from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from products.models import Product


@registry.register_document
class ProductDocument(Document):
    inventory = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "quantity_sold": fields.IntegerField(),
            "total": fields.IntegerField(),
            "available_quantity": fields.IntegerField(attr="get_available_quatity"),
        }
    )

    category = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "slug": fields.TextField(),
            "is_active": fields.BooleanField(),
        }
    )

    subcategory = fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "category": category,
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
        }
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
        ]
