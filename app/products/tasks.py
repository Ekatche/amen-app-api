from decimal import Decimal
from math import ceil
from datetime import datetime
from celery import shared_task
from django.db import transaction
from .models import Product, Promotion


@shared_task()
def promotion_price(reduction_amount, object_id):
    """
    this function apply a promotion to a product
    :param reduction_amount: reduction amount
    :param object_id: promotion id
    :return: product with price updated
    """
    with transaction.atomic():
        promotion = Product.objects.filter(promo=object_id)
        reduction = reduction_amount / 100
        for product in promotion:
            if product.on_promo:
                price = product.price
                new_price = ceil(price - (price * Decimal(reduction)))
                product.promo_price = Decimal(new_price)
                product.save()


@shared_task()
def promotion_management():
    with transaction.atomic():
        promotions = Promotion.objects.filter(is_schedule=True)

        now = datetime.now().date()

        for promo in promotions:
            if promo.date_end < now:
                promo.is_active = False
                promo.is_schedule = False
            else:
                if promo.date_start <= now:
                    promo.is_active = True
                else:
                    promo.is_active = False
            promo.save()
