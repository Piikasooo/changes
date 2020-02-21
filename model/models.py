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
    from_date = models.DateField()
    until_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('currency', 'from_date'),)

    def __str__(self):
        return f'{self.from_date} {self.until_date if self.until_date else ""} {self.purchase} {self.selling}'

    def get_all_history(currency):
        return ExchangeHistory.objects.filter(currency=currency)


        
