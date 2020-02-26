import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils.timezone import now
from .models import ExchangeHistory, Currency


class TestExchanceHistory(TestCase):
    fixtures = ['history_testdata.json']

    def setUp(self):
        self.currency = Currency.objects.get(currency="USD")

    def test_add(self):
        add_rate = ExchangeHistory.objects.create(
            currency=self.currency,
            purchase=34.21,
            selling=35.89,
            from_date=now().date()
        )
        prev = ExchangeHistory.objects.get(
            currency=self.currency,
            from_date=datetime.date(2019, 2, 10)
        )
        self.assertEqual(add_rate.until_date, None)
        self.assertEqual(add_rate.from_date, now().date())
