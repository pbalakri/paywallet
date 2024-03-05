from django.db import models
import uuid

from product.models import Product
from .cafe import Cafe
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


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
            [item.original_price * item.quantity for item in self.orderitem_set.all()])
        return str(self.date) + " - " + str(order_total)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, default=None)
    quantity = models.IntegerField()
    original_price = models.FloatField()
    selling_price = models.FloatField()
    currency = models.CharField(max_length=10, default='KWD')

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return self.product.name + " (" + str(self.quantity) + ") "


class OrderItemInlines(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cafe', 'date', 'order_total', 'payment_method')
    fields = ('cafe', 'payment_method')
    inlines = [OrderItemInlines]

    def order_total(self, obj):
        return '%.3f KWD' % sum([item.original_price * item.quantity for item in obj.orderitem_set.all()])

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(cafe__admin=request.user)
