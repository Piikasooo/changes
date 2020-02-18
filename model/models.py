from django.db import models, IntegrityError
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist


class Currency(models.Model):
    currency = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.currency


class ExchangeHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_history')
    purchase = models.DecimalField(max_digits=5, decimal_places=2)
    selling = models.DecimalField(max_digits=5, decimal_places=2)
    from_data = models.DateField()
    until_data = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('currency', 'from_data'),)

    def change(self, that_change):
        that_change.until_data = self.from_data - timedelta(days=1)
        that_change.save()

    def previous(self):
        return ExchangeHistory.objects.filter(currency=self.currency, from_data__lt=self.from_data).latest('from_data')

    def last(self):
        return ExchangeHistory.objects.filter(currency=self.currency).latest('from_data')

    def first(self):
        return ExchangeHistory.objects.filter(currency=self.currency).latest('-from_data')

    def save(self, *args, **kwargs):
        if self.until_data is not None and self.from_data > self.until_data:
            raise IntegrityError
        if not self.id:
            try:
                first = self.first()
                if first.from_data > self.from_data and\
                        (self.until_data is None or first.from_data > self.until_data):
                    self.until_data = first.from_data - timedelta(days=1)
                elif first.from_data < self.from_data:
                    last = self.last()
                    if (last.until_data is None or last.until_data < self.from_data) \
                            and last.from_data < self.from_data:
                        self.change(last)
                    else:
                        previous = self.previous()
                        if self.until_data is None or previous.until_data > self.until_data:
                            self.until_data = previous.until_data
                        self.change(previous)
                else:
                    raise IntegrityError
            except ObjectDoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.first() != self:
            previous = self.previous()
            if previous and self != self.last():
                previous.until_data = self.until_data
                previous.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.currency)
