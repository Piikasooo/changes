from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
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

    def _first(self):
        return ExchangeHistory.objects.filter(currency=self.currency).earliest('from_date')

    def _last(self):
        return ExchangeHistory.objects.filter(currency=self.currency).latest('from_date')

    def _prev(self):
        return ExchangeHistory.objects.filter(currency=self.currency, from_date__lt=self.from_date).latest('from_date')

    def _change(self, change_obj):
        change_obj.until_date = self.from_date - timedelta(days=1)
        change_obj.save()

    def save(self, *args, **kwargs):
        if self.until_date is not None and self.until_date < self.from_date:
            raise IntegrityError
        if not self.id:
            try:
                first = self._first()
                if is_valid(self.from_date, first.from_date, self.until_date):
                    self.until_date = first.from_date - timedelta(days=1)
                elif self.from_date > first.from_date:
                    last = self._last()
                    if is_valid(last.from_date, self.from_date, last.until_date):
                        self._change(last)
                    else:
                        prev = self._prev()
                        if self.until_date is None or self.until_date < prev.until_date:
                            self.until_date = prev.until_date
                        self._change(prev)
                else:
                    raise IntegrityError
            except ObjectDoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self._first() != self:
            prev = self._prev()
            if self != self._last() and prev:
                prev.until_date = self.until_date
                prev.save()
        super().delete(*args, **kwargs)


def is_valid(firstrate_fromdate, secondrate_fromdate, until_date):
    return firstrate_fromdate < secondrate_fromdate and (until_date is None or until_date < secondrate_fromdate)
