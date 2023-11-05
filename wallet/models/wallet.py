from django.db import models
from django.contrib import admin

from .bracelet import Bracelet


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.IntegerField(default=0)
    bracelet_id = models.ForeignKey(
        Bracelet, on_delete=models.RESTRICT, null=True)


# class WalletAdmin(admin.ModelAdmin):
#     list_display = ('balance')
#     fields = ('balance')
