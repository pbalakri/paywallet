from django.db import models
import uuid

from product.models import Product
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import Inventory, Cafe


class Order(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    cafe = models.ForeignKey(Cafe, on_delete=models.RESTRICT)
    date = models.DateField(auto_now_add=True)
    payment_choices = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('points', 'Points'),
    ]
    payment_method = models.CharField(
        max_length=10, choices=payment_choices, default='cash')

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        order_total = '%.3f KWD' % sum(
            [item.product.price * item.quantity for item in self.orderitem_set.all()])
        return str(self.date) + " - " + str(order_total)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Inventory, on_delete=models.RESTRICT, default=None)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return self.product.product.name + " (" + str(self.quantity) + ") "


class OrderItemInlines(admin.TabularInline):
    list_display = ('product', 'quantity', 'price')

    def price(self, obj):
        return '%.3f KWD' % (obj.product.price * obj.quantity)
    model = OrderItem
    extra = 0


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order', 'price')
    fields = ('product', 'quantity', 'order')

    def price(self, obj):
        return '%.3f KWD' % (obj.product.price * obj.quantity)

    def get_queryset(self, request):
        qs = super(OrderItemAdmin, self).get_queryset(request)

        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return qs
        else:
            return qs.filter(order__cafe__admin=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return super(OrderItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "order":
            kwargs["queryset"] = Order.objects.filter(cafe__admin=request.user)
            return super(OrderItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == 'product':
            # Hide products that already have quantity in the inventory
            kwargs["queryset"] = Inventory.objects.filter(
                cafe__admin=request.user)
            return super(OrderItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(OrderItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cafe', 'date', 'order_total', 'payment_method')
    fields = ('cafe', 'payment_method')
    inlines = [OrderItemInlines]
    list_filter = ['cafe__name', 'date']

    def order_total(self, obj):
        return '%.3f KWD' % sum([item.product.price * item.quantity for item in obj.orderitem_set.all()])

    def get_fields(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return ('cafe', 'payment_method')
        else:
            return ('payment_method',)

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)

        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return qs
        else:
            return qs.filter(cafe__admin=request.user)
