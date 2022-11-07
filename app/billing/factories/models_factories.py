import factory
from ..models import Invoice
from order.factories import OrderFactory
from factory.django import DjangoModelFactory
from core.factories import BillingAddressFactory


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice

    billing = factory.RelatedFactory(
        BillingAddressFactory, factory_related_name="invoice"
    )
    order = factory.RelatedFactory(OrderFactory, factory_related_name="order_invoice")
    payment_method = "Card"
    amount_due = 15
    amount_paid = 15
    status = "Payed"
