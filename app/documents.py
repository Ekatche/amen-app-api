from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from .inventory.models import Inventory


@registry.register_document
class ProductDocument(Document):
    inventory = fields.ObjectField(
        properties={
            "name": fields.IntegerField(),
        }
    )

    class Index:
        # Name of the Elasticsearch index
        name = "inventory"

        class Django:
            model = Inventory
            fields = [
                "id",
                "quantity_sold",
                "total",
            ]
