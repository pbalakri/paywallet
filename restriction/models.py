import uuid
from django.db import models
from school.models import Student
from django.utils.translation import gettext_lazy as _
from product.models import Category, Product, Allergy
from django.contrib import admin
from school.models import Bracelet


class FrequencyRestriction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    total_per_period = models.FloatField(default=3)
    restriction_frequency = (
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
    )
    frequency = models.CharField(
        max_length=10, choices=restriction_frequency, default='Weekly')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DietRestriction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    allergies = models.ManyToManyField(
        Allergy, blank=True)

    def __str__(self):
        return ', '.join([a.name for a in self.allergies.all()])

    class Meta:
        verbose_name = _('Diet Restriction')
        verbose_name_plural = _('Diet Restrictions')


class DietRestrictionAdmin(admin.ModelAdmin):
    list_display = ('student', 'all_allergies')
    fields = ('student', 'allergies')
    search_fields = ('student',)

    def all_allergies(self, obj):
        return ', '.join([a.name for a in obj.allergies.all()])


class CategoryRestriction(FrequencyRestriction):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = _('Category Restriction')
        verbose_name_plural = _('Category Restrictions')


class CategoryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'total_per_period', 'frequency')
    fields = ('student', 'category', 'total_per_period', 'frequency')
    search_fields = ('student',)


class PaymentRestriction(FrequencyRestriction):
    def __str__(self):
        return self.frequency

    class Meta:
        verbose_name = _('Payment Restriction')
        verbose_name_plural = _('Payment Restrictions')


class PaymentRestrictionAdmin(admin.ModelAdmin):
    list_display = ('student', 'total_per_period', 'frequency')
    fields = ('student', 'total_per_period', 'frequency')
    search_fields = ('student',)


class ProductsRestriction(FrequencyRestriction):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Product Restriction')
        verbose_name_plural = _('Product Restrictions')


class ProductsRestrictionAdmin(admin.ModelAdmin):
    list_display = ('student', 'product', 'total_per_period', 'frequency')
    fields = ('student', 'product', 'total_per_period', 'frequency')
    search_fields = ('student',)
