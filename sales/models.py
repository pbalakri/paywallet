import uuid
from django.db import models
from cafe.models import Cafe
from django.contrib import admin


class Sale(models.Model):
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
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return str(self.date) + " - " + str(self.total)


class SoldItems(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    original_price = models.FloatField()
    selling_price = models.FloatField()
    currency = models.CharField(max_length=10, default='KWD')

    class Meta:
        verbose_name = "Sold Item"
        verbose_name_plural = "Sold Items"

    def __str__(self):
        return self.product_id.name + " - " + str(self.quantity)


class SoldItemInlines(admin.TabularInline):
    model = SoldItems
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'total', 'payment_method')
    fields = ('cafe_id', 'payment_method')
    inlines = [SoldItemInlines]

    def get_queryset(self, request):
        qs = super(SaleAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(cafe_id__vendor_admin=request.user)
