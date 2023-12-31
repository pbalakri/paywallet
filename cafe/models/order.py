from django.db import models
import uuid
from .cafe import Cafe
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    cafe_id = models.ForeignKey(Cafe, on_delete=models.RESTRICT)
    date = models.DateField(auto_now_add=True)
    total = models.FloatField()
    currency = models.CharField(max_length=10, default='KWD')
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
        return str(self.date) + " - " + str(self.total)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    original_price = models.FloatField()
    selling_price = models.FloatField()
    currency = models.CharField(max_length=10, default='KWD')

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return self.product_id.name + " - " + str(self.quantity)


class OrderItemInlines(admin.TabularInline):
    readonly_fields = ['product_name', 'quantity',
                       'original_price', 'selling_price']
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'total', 'payment_method')
    fields = ('cafe_id', 'payment_method')
    inlines = [OrderItemInlines]

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(cafe_id__vendor_admin=request.user)
