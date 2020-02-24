from django.db import models
from datetime import timedelta, datetime


class Currency(models.Model):
    currency = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.currency


class ExchangeHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_history')
    purchase = models.DecimalField(max_digits=5, decimal_places=2)
    selling = models.DecimalField(max_digits=5, decimal_places=2)
    from_date = models.DateField()
    until_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['from_date']

    def __str__(self):
        return f'{self.from_date} {self.until_date if self.until_date else ""} {self.purchase} {self.selling}'


def get_all_currency_history(currency):
    return ExchangeHistory.objects.filter(currency=currency)


def add_rate(from_date, purchase, selling, currency_id, until_date):
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    currency = Currency.objects.get(id=currency_id)
    last_rate = get_all_currency_history(currency).last()
    last_rate.until_date = (from_date - timedelta(days=1))
    last_rate.save()
    new_rate = ExchangeHistory(from_date=from_date, purchase=purchase, selling=selling,
                               until_date=until_date, currency_id=currency_id)
    new_rate.save()
    return new_rate


def insert_rate(from_date, purchase, selling, currency):
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    id = None
    history = get_all_currency_history(currency)
    for rate in history:
        if rate.from_date <= from_date.date():
            id = rate.id
        else:
            break
    update_rate = ExchangeHistory.objects.get(id=id)
    ins_rate = ExchangeHistory(from_date=from_date , until_date=update_rate.until_date, purchase=purchase,
                               selling=selling, currency=currency)
    update_rate.until_date = from_date - timedelta(days=1)
    update_rate.save()
    ins_rate.save()
    return ins_rate


def delete_rate(rate_id):
    rate = ExchangeHistory.objects.get(id=rate_id)
    rate.delete()
    return rate



