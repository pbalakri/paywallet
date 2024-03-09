from datetime import datetime, timedelta
from typing import Any
from django.db import models
import uuid

from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from cafe.models import Cafe
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
    merchant = models.ForeignKey(
        Cafe, on_delete=models.RESTRICT)
    reference = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.type == 'debit':
            wallet = Wallet.objects.get(bracelet_id=self.wallet.bracelet_id)
            if wallet.balance < self.amount:
                raise Exception('Insufficient balance')
            else:
                wallet.balance -= self.amount

        else:
            wallet = Wallet.objects.get(bracelet_id=self.wallet.bracelet_id)
            wallet.balance += self.amount
        with transaction.atomic():
            wallet.save()
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount',
                    'merchant', 'reference')
    fields = ('type', 'amount', 'wallet',
              'merchant', 'reference')

    def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "merchant":
            kwargs["queryset"] = Cafe.objects.filter(
                vendor_admin=request.user)
            return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(TransactionAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return qs
        else:
            return qs.filter(merchant__vendor_admin=request.user)
