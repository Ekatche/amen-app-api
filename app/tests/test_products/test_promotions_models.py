from django.test import TestCase
from products.models import Promotion, Coupons
from model_bakery import baker
from products.factories import PromotionFactory


class PromotionModelTest(TestCase):
    """
    test promotions and coupons
    test promotions associated with coupons
    """

    def setUp(self):
        # promotion without attaching it to a coupons
        self.promotion = baker.make(Promotion, name="OCTOBERTEST", period=2)

        # coupons without promotion attached
        self.coupons = baker.make(
            Coupons, name="ThirtyPercent", code="MOINS0", discount=30, is_active=True
        )

    def test_create_promotion(self):
        """TEst creating promotion"""
        self.assertEqual(self.promotion.name, "OCTOBERTEST")

    def test_create_coupons(self):
        """Test creating promotion"""
        self.assertEqual(self.coupons.name, "ThirtyPercent")

    def test_create_coupons_and_associate_to_promo(self):
        """Test creating coupons associated with coupons"""
        # coupons attached to promotion
        promo = PromotionFactory(name="OCTOBERTEST22", coupons=self.coupons)

        self.assertEqual(promo.name, "OCTOBERTEST22")
        self.assertEqual(promo.coupons.name, "ThirtyPercent")
