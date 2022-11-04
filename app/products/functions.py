from .models import (
    Promotion,
)
from dateutil.relativedelta import relativedelta
from datetime import datetime


def calculateNewPrice(product, promotion, coupons):
    """
    Compute new price for product that are in promotion
    :param product:
    :param promotion:
    :param coupons:
    :return: compute new price and return True
    """
    # avoir les produits
    # si produits en promo
    # prendre la promotion
    # calculer nouveau prix et afficher nouveaux prix
    return True


def calculateNewEndDate(period, old_date=None, as_timestamp=True):
    timestamp_now = int(datetime.now().timestamp())

    if old_date is None or old_date < timestamp_now:
        old_date = timestamp_now

    new_end_date = datetime.fromtimestamp(old_date) + relativedelta(months=period)
    if as_timestamp:
        new_end_date = int(new_end_date.timestamp())
    return new_end_date


def updateEndDate(promotion):
    try:
        coupons = Promotion.objects.get(id=promotion)  # noqa
    except Promotion.DoesNotExist:
        return False

    new_end_date = calculateNewEndDate(
        promotion.period,
        old_date=int(
            datetime(
                year=promotion.date_end.year,
                month=promotion.date_end.month,
                day=promotion.date_end.day,
            ).timestamp()
        ),
        as_timestamp=True,
    )

    promotion.date_end = datetime.fromtimestamp(new_end_date)
    promotion.save()

    return True
