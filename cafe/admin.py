from django.contrib import admin
from .models import Cafe, Inventory, InventoryAdmin, CafeAdmin, Order, OrderAdmin, Dashboard, DashboardAdmin
# Register your models here.
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Dashboard, DashboardAdmin)
