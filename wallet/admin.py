from django.contrib import admin

# Register your models here.
from .models import Transaction, Bracelet, TransactionAdmin, BraceletAdmin, PaymentRestriction, CategoryRestriction, Device, DeviceAdmin
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Bracelet, BraceletAdmin)
admin.site.register(PaymentRestriction)
admin.site.register(CategoryRestriction)
admin.site.register(Device, DeviceAdmin)
