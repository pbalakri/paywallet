from django.contrib import admin
from .models import Cafe, Inventory, InventoryAdmin, CafeAdmin, Order, OrderAdmin, Operator, OperatorAdmin, VendorAdmin, VendorAdminAdmin
# Register your models here.
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(VendorAdmin, VendorAdminAdmin)
