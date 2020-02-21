from django.shortcuts import render, get_object_or_404

from .models import Currency, ExchangeHistory


def get_index_page(request):
    currencies = Currency.objects.all()
    return render(request, 'model/index.html', {'currencies': currencies})


def get_currency_history(request, currency_name):
    currency = get_object_or_404(Currency, currency=currency_name)
    history = ExchangeHistory.objects.all()   #filter(currency=currency)
    return render(request, 'model/currency.html', {'currency': currency,
                                                     'history': history})