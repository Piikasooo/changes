from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta


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

    def get_next_rate(self):
        """
        Getting the rate is the from_date which is later than the rate from_date we are trying to enter
        """
        try:
            return ExchangeHistory.objects.filter(currency=self.currency,
                                                  from_date__gt=self.from_date).latest('from_date')
        except ObjectDoesNotExist:
            return None

    def get_previous_rate(self):
        """
        Getting the rate is the from_date which is earlier than the rate from_date we are trying to enter
        """
        try:
            return ExchangeHistory.objects.filter(currency=self.currency,
                                                  from_date__lt=self.from_date).latest('from_date')
        except ObjectDoesNotExist:
            return None

    def change(self, change_obj):
        """Change rate until_from when add/delete new rate"""
        change_obj.until_date = self.from_date - timedelta(days=1)
        change_obj.save()

    def save(self, *args, **kwargs):
        if self.until_date is not None and self.until_date < self.from_date:
            raise IntegrityError
        if not self.id:
            previous_rate = self.get_previous_rate()
            next_rate = self.get_next_rate()
            if previous_rate is None:
                next_rate.change(self)
            elif next_rate is None:
                self.change(previous_rate)
            else:
                previous_rate.until_date = self.from_date - timedelta(days=1)
                previous_rate.save()
                self.until_date = next_rate.from_date - timedelta(days=1)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        previous_rate = self.get_previous_rate()
        next_rate = self.get_next_rate()
        if previous_rate is not None and next_rate is not None:
            previous_rate.until_date = self.until_date
            previous_rate.save()
        super().delete(*args, **kwargs)
