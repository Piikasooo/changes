from django.contrib import admin
from .models import Currency, ExchangeHistory

admin.site.register(ExchangeHistory)
admin.site.register(Currency)
