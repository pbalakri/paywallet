from django.db import models
import uuid
from product.models import Product
from . import Cafe
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import random


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
        return self.product.name + " (" + str(self.product_code) + ") "


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'product', 'quantity',
                    'price')
    fields = (('product_code', 'product'), ('quantity', 'price'), 'cafe')
    search_fields = ('product__name', 'cafe__name', 'product_code')
    list_editable = ('quantity', 'price')
    change_list_template = 'admin/cafe/inventory/change_list.html'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "cafe":
            kwargs["queryset"] = Cafe.objects.filter(
                admin=request.user)
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == 'product':
            # Hide products that already have quantity in the inventory
            kwargs["queryset"] = Product.objects.exclude(
                inventory__quantity__gt=0)
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(InventoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_display(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            # Add cafe to list
            new_list_display = list(self.list_display)
            new_list_display.append('cafe')
            return new_list_display
        else:
            return super(InventoryAdmin, self).get_list_display(request)

    def get_queryset(self, request):
        qs = super(InventoryAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return qs
        elif request.user.groups.filter(name='Vendor Admin').exists():
            return qs.filter(cafe__admin=request.user)
        elif request.user.groups.filter(name='Vendor Operator').exists():
            return qs.filter(cafe__operators=request.user)

    def getRandomColor(self):
        letters = list('0123456789ABCDEF')
        color = '#'
        for i in range(6):
            f = random.randint(0, 15)
            color += letters[f]
        return color

    def get_product_count_based_on_stock(self, qs):
        labels = []
        data = []
        background_color = []
        #  Get product count based on stock whether it is in stock or out of stock

        in_stock_count = qs.filter(quantity__gt=5).count()
        if (in_stock_count > 0):
            labels.append('In Stock')
            data.append(in_stock_count)
            background_color.append(self.getRandomColor())

        low_stock_count = qs.filter(quantity__gt=0, quantity__lte=5).count()
        if (low_stock_count > 0):
            labels.append('Low Stock')
            data.append(low_stock_count)
            background_color.append(self.getRandomColor())

        oos_count = qs.filter(quantity=0).count()
        if (oos_count > 0):
            labels.append('OOS')
            data.append(oos_count)
            background_color.append(self.getRandomColor())

        return {
            'labels': labels,
            'datasets': [{'data': data,
                         'backgroundColor': background_color}]
        }

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            response.context_data['get_product_count_based_on_stock'] = self.get_product_count_based_on_stock(
                qs)
        except (AttributeError, KeyError):
            return response
        return response
