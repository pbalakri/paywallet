from typing import Any
from django.db import models
import uuid

from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from cafe.models import Cafe
from .bracelet import Bracelet
from django.contrib import admin
from django.db import transaction


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # type is either 'credit' or 'debit'
    typeChoices = [('credit', 'credit'), ('debit', 'debit')]
    type = models.CharField(max_length=10, choices=typeChoices)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    bracelet_id = models.ForeignKey(
        Bracelet, on_delete=models.RESTRICT)
    merchant_id = models.ForeignKey(
        Cafe, on_delete=models.RESTRICT)
    reference = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.type == 'debit':
            bracelet = Bracelet.objects.get(rfid=self.bracelet_id)
            if bracelet.balance < self.amount:
                raise Exception('Insufficient balance')
            else:
                bracelet.balance -= self.amount

        else:
            bracelet = Bracelet.objects.get(rfid=self.bracelet_id)
            bracelet.balance += self.amount
        with transaction.atomic():
            bracelet.save()
            super().save(*args, **kwargs)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount',
                    'merchant_id', 'reference')
    fields = ('type', 'amount', 'bracelet_id',
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
