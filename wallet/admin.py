from django.contrib import admin

# Register your models here.
from .models import Transaction, Bracelet, TransactionAdmin, BraceletAdmin
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Bracelet, BraceletAdmin)
