from typing import Any
from django.db import models
import uuid
from django.contrib import admin
from django.conf import settings
from school.models import School
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(
        School, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class CategoryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "school":
            kwargs["queryset"] = School.objects.filter(
                school_admin=request.user)
            return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(school__school_admin=request.user)


class Product(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True)
    school = models.ForeignKey(
        School, on_delete=models.RESTRICT, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, blank=True, null=True)
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductAdmin(admin.ModelAdmin):
    fields = (('name', 'image'), 'description', ('price', 'stock'),
              ('category', 'is_active'), 'school')
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "school":
            kwargs["queryset"] = School.objects.filter(
                school_admin=request.user)
            return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(
                school__school_admin=request.user)
            return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class Order(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, limit_choices_to={
        'groups__name': 'Guardian'}, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status_choices = [('Pending', 'Pending'),
                      ('Ready for Pickup', 'Ready for Pickup'),
                      ('Completed', 'Completed'),
                      ('Cancelled', 'Cancelled')]
    status = models.CharField(
        max_length=20, choices=status_choices, default='Pending')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.RESTRICT, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class OrderItemInlines(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'quantity', 'product']


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInlines]
