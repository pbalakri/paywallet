import uuid
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from school.models import Bracelet


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bracelet = models.ForeignKey(
        Bracelet, on_delete=models.RESTRICT, default=None)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.bracelet.rfid

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('bracelet',)
    fields = ('bracelet',)
    search_fields = ('bracelet',)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return super().get_list_display(request) + ('balance',)
        else:
            return super().get_list_display(request)

    def get_fields(self, request, obj):
        if request.user.is_superuser:
            return super().get_fields(request, obj) + ('balance',)
        else:
            return super().get_fields(request, obj)
