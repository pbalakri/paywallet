from django.db import models
import uuid
from product.models import Product
from . import Cafe
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class Inventory(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.FloatField()
    currency = models.CharField(max_length=10, default='KWD')
    cafe = models.ForeignKey(Cafe, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventory")

    def __str__(self):
        return self.product.name


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity',
                    'product_price', 'cafe', 'currency')
    fields = ('product', 'quantity', 'price', 'cafe', 'currency')
    search_fields = ('product__name', 'cafe__name')
    readonly_fields = ('currency',)

    def product_price(self, obj):
        return '%.3f KWD' % obj.price

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "cafe":
            kwargs["queryset"] = Cafe.objects.filter(
                vendor_admin=request.user)
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(InventoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Vendor Admin').exists():
            return qs.filter(cafe_id__vendor_admin=request.user)
        elif request.user.groups.filter(name='Vendor Operator').exists():
            return qs.filter(cafe_id__vendor_operators=request.user)
