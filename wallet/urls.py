from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"wallets/<str:rfid>/balance",
         views.BalanceView.as_view(), name="balance"),
    path(r"wallets/<str:rfid>/transactions",
         views.TransactionsView.as_view(), name="transactions"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
