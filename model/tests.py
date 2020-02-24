import datetime
from django.test import TestCase
from django.utils.timezone import now
from .models import ExchangeHistory, Currency, add_rate


class TestExchangeHistory(TestCase):
    fixtures = ['history_testdata.json']

    def setUp(self):
        self.currency = Currency.objects.get(currency="USD")

    def test_add_rate(self):
        adding_exchange_rate = add_rate(from_date=str(now().date()), purchase=24.75, selling=25.15,
                                        currency_id=1, until_date=str(now().date()))

        self.assertEquals(adding_exchange_rate.from_date, now().date())

