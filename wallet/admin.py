from django.contrib import admin

# Register your models here.
from .models import Transaction, Wallet, TransactionAdmin, WalletAdmin, TopUp, TopUpAdmin
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(TopUp, TopUpAdmin)
