from datetime import datetime, timedelta
from typing import Any
from django.db import models
import uuid

from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from cafe.models import Cafe
from restriction.models import CategoryRestriction, PaymentRestriction
from .wallet import Wallet
from django.contrib import admin
from django.db import transaction
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # type is either 'credit' or 'debit'
    typeChoices = [('credit', 'credit'), ('debit', 'debit')]
    type = models.CharField(max_length=10, choices=typeChoices)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.RESTRICT)
    merchant_id = models.ForeignKey(
        Cafe, on_delete=models.RESTRICT)
    reference = models.CharField(max_length=100, blank=True, null=True)

    def check_for_payment_restrictions(self):
        # Get all payment restrictions for this wallet

        restrictions = PaymentRestriction.objects.filter(
            wallet=self.wallet)
        for restriction in restrictions:
            # check if frequency of restriction is weekly
            if restriction.frequency == 'Weekly':
                # get total count of transactions this week of year
                transactions_this_week = Transaction.objects.filter(
                    wallet=self.wallet, date__week=datetime.today().isocalendar()[1])
                if transactions_this_week.count() > restriction.count_per_period:
                    raise Exception(
                        'You have exceeded your weekly transaction limit')
            elif restriction.frequency == 'Monthly':
                # get total count of transactions this month
                transactions_this_month = Transaction.objects.filter(
                    wallet=self.wallet, date__month=datetime.now().month)
                if transactions_this_month.count() > restriction.count_per_period:
                    raise Exception(
                        'You have exceeded your monthly transaction limit')
            elif restriction.frequency == 'Daily':
                # get total count of transactions today
                transactions_today = Transaction.objects.filter(
                    wallet=self.wallet, date__day=datetime.now().day)
                if transactions_today.count() > restriction.count_per_period:
                    raise Exception(
                        'You have exceeded your daily transaction limit')

        return True

    def check_for_category_restrictions(self):
        # Get all category restrictions for this wallet
        restrictions = CategoryRestriction.objects.filter(
            wallet=self.wallet)
        return True

    def save(self, *args, **kwargs):
        if self.type == 'debit':
            self.check_for_payment_restrictions()
            wallet = Wallet.objects.get(rfid=self.wallet)
            if wallet.balance < self.amount:
                raise Exception('Insufficient balance')
            else:
                wallet.balance -= self.amount

        else:
            wallet = Wallet.objects.get(rfid=self.wallet)
            wallet.balance += self.amount
        with transaction.atomic():
            wallet.save()
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount',
                    'merchant_id', 'reference')
    fields = ('type', 'amount', 'wallet',
              'merchant_id', 'reference')

    def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
        if request.user.is_superuser:
            return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "merchant_id":
            kwargs["queryset"] = Cafe.objects.filter(
                vendor_admin=request.user)
            return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(TransactionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(merchant_id__vendor_admin=request.user)
