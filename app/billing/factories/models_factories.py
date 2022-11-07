import factory
from ..models import Invoice
from order.factories import OrderFactory
from factory.django import DjangoModelFactory
from core.factories import BillingAddressFactory


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice

    billing = factory.SubFactory(BillingAddressFactory)
    order = factory.SubFactory(OrderFactory)
    payment_method = "Card"
    amount_due = 15
    amount_paid = 15
    status = "Payed"
