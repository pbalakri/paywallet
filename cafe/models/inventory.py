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
    product_code = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.FloatField()
    cafe = models.ForeignKey(Cafe, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventory")
        unique_together = ('product_code', 'cafe')

    def __str__(self):
        return self.product.name


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'product', 'quantity',
                    'product_price', 'cafe')
    fields = (('product_code', 'product'), ('quantity', 'price'), 'cafe')
    search_fields = ('product__name', 'cafe__name', 'product_code')

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
