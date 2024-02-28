import uuid
from django.db import models
from school.models import Student
from django.utils.translation import gettext_lazy as _
from product.models import Category, Product, Allergy


class Restriction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # Set this to proxy model
    class Meta:
        abstract = True


class DietRestriction(Restriction):
    allergies = models.ManyToManyField(
        Allergy, blank=True)

    def __str__(self):
        return self.dietary_restriction

    class Meta:
        verbose_name = _('Diet Restriction')
        verbose_name_plural = _('Diet Restrictions')


class CategoryRestriction(Restriction):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = _('Category Restriction')
        verbose_name_plural = _('Category Restrictions')


class PaymentRestriction(Restriction):
    count_per_period = models.IntegerField(default=3)
    restriction_frequency = (
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
    )
    frequency = models.CharField(
        max_length=10, choices=restriction_frequency, default='Weekly')

    def __str__(self):
        return self.frequency

    class Meta:
        verbose_name = _('Payment Restriction')
        verbose_name_plural = _('Payment Restrictions')


class ProductRestriction(Restriction):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Product Restriction')
        verbose_name_plural = _('Product Restrictions')
