from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"balance",
         views.BalanceView.as_view(), name="balance"),
    path(r"transactions",
         views.TransactionsView.as_view(), name="transactions"),
    path(r"topups",
         views.TopupsView.as_view(), name="topups"),
    path(r"restrictions",
         views.PurchaseRestrictionView.as_view(), name="restrictions"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
