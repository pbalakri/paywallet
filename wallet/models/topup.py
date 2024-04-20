
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
    amount = models.FloatField(default=0)
    reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # On save, increment wallet balance by amount

    def save(self, *args, **kwargs):
        wallet = Wallet.objects.get(bracelet_id=self.wallet.bracelet_id)
        wallet.balance += self.amount
        wallet.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f' {self.amount}'


class TopUpAdmin(admin.ModelAdmin):
    list_display = ('guardian', 'wallet', 'amount', 'reference', 'created_at')
    search_fields = ('guardian__user__first_name', 'guardian__user__last_name',
                     'wallet__bracelet_id', 'amount', 'reference')
    list_filter = ('created_at',)
