from django.urls import path

from .views import get_index_page, get_currency_history

urlpatterns = [
    path('', get_index_page, name="index"),
    path('<currency_name>', get_currency_history, name="currency"),
]