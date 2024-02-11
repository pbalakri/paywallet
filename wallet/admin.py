from django.contrib import admin

# Register your models here.
from .models import Transaction, Wallet, TransactionAdmin, WalletAdmin
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
