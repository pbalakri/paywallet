from django.contrib import admin
from .models import Cafe, Inventory, InventoryAdmin, CafeAdmin
# Register your models here.
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Inventory, InventoryAdmin)
