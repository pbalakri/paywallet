from django.contrib import admin
from .models import Sale, SoldItems, SaleAdmin

admin.site.register(Sale, SaleAdmin)
admin.site.register(SoldItems)
# Register your models here.
