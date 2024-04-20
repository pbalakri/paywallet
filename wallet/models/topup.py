
from django.db import models
import uuid
from django.contrib import admin
from guardian.models import Guardian
from .wallet import Wallet


class TopUp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guardian = models.ForeignKey(
        Guardian, on_delete=models.RESTRICT)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'


class TopUpAdmin(admin.ModelAdmin):
    list_display = ('guardian', 'wallet', 'amount', 'reference', 'created_at')
    search_fields = ('guardian__user__first_name', 'guardian__user__last_name',
                     'wallet__bracelet_id', 'amount', 'reference')
    list_filter = ('created_at',)
