import datetime
from django.test import TestCase
from django.utils.timezone import now
from .models import ExchangeHistory, Currency


class TestExchangeHistory(TestCase):
    fixtures = ['history_testdata.json']

    def setUp(self):
        self.currency = Currency.objects.get(currency="USD")

    def test_add_rate(self):
        adding_exchange_rate = ExchangeHistory.objects.create(
            currency=self.currency,
            purchase_rate=24.75,
            selling_rate=25.15,
            valid_from=now().date())

        previous_exchange_rate = ExchangeHistory.objects.get(
            currency=self.currency,
            valid_from=datetime.date(2020, 1, 15))

        self.assertEquals(adding_exchange_rate.valid_until, None)
        self.assertEquals(adding_exchange_rate.valid_from, now().date())
        self.assertEquals(previous_exchange_rate.valid_until,
                          adding_exchange_rate.valid_from - datetime.timedelta(days=1))
