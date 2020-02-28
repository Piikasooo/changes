import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils.timezone import now
from .models import ExchangeHistory, Currency


class TestExchangeHistory(TestCase):
    fixtures = ['history_testdata.json']

    def setUp(self):
        self.currency = Currency.objects.get(currency="USD")

    def test_add_today(self):
        add_rate = ExchangeHistory.objects.create(
            currency=self.currency,
            purchase=34.21,
            selling=35.89,
            from_date=now().date()
        )
        prev = ExchangeHistory.objects.get(
            currency=self.currency,
            from_date=datetime.date(2019, 3, 15)
        )
        self.assertEqual(add_rate.until_date, None)
        self.assertEqual(add_rate.from_date, now().date())
        self.assertEqual(prev.until_date, add_rate.from_date - datetime.timedelta(days=1))

    def test_add_from_date(self):
        add_rate = ExchangeHistory.objects.create(
            currency=self.currency,
            purchase=34.21,
            selling=35.89,
            from_date=datetime.date(2019, 2, 20)
        )
        prev = ExchangeHistory.objects.get(
            currency=self.currency,
            from_date=datetime.date(2019, 2, 10)
        )
        self.assertEqual(add_rate.from_date, datetime.date(2019, 2, 20))
        self.assertEqual(add_rate.until_date, datetime.date(2019, 3, 14))
        self.assertEqual(prev.until_date, datetime.date(2019, 2, 19))

    def test_delete(self):
        remove_rate = ExchangeHistory.objects.get(
            currency=self.currency,
            from_date=datetime.date(2019, 2, 10)
        )
        remove_rate.delete()
        prev = ExchangeHistory.objects.get(
            currency=self.currency,
            from_date=datetime.date(2019, 1, 30)
        )
        with self.assertRaises(ObjectDoesNotExist):
            ExchangeHistory.objects.get(
                currency=self.currency,
                from_date=datetime.date(2019, 2, 10)
            )
        self.assertEqual(prev.until_date, datetime.date(2019, 3, 14))
