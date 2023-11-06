from django.db import models
from .bracelet import Bracelet
from product.models import Category
from django.utils.translation import gettext_lazy as _


class PaymentRestriction(models.Model):
    id = models.AutoField(primary_key=True)
    count_per_period = models.IntegerField(default=3)
    restriction_frequency = (
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
    )
    frequency = models.CharField(
        max_length=10, choices=restriction_frequency, default='Weekly')
    bracelet = models.ForeignKey(
        Bracelet, on_delete=models.CASCADE)

    def __str__(self):
        return self.frequency

    class Meta:
        verbose_name = _('Payment Restriction')
        verbose_name_plural = _('Payment Restrictions')


class CategoryRestriction(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    bracelet = models.ForeignKey(
        Bracelet, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Category Restriction')
        verbose_name_plural = _('Category Restrictions')
