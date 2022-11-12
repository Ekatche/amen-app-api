from billing.factories import InvoiceFactory
from django.test import TestCase
from billing.models import Invoice


class InvoiceModelTest(TestCase):
    def setUp(self) -> None:
        InvoiceFactory()
        InvoiceFactory()

    def test_invoice_creation(self):
        invoice = Invoice.objects.all()
        self.assertTrue(len(invoice) > 1)
