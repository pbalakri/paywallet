# Create a model to store restrictions for a user
# Payment restrictions are Once Per Week, Once Per Day, Once Per Month
# Category restrictions prevent a user from purchasing a product in a category
from django.db import models

from .bracelet import Bracelet
from product.models import Category


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


class CategoryRestriction(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    bracelet = models.ForeignKey(
        Bracelet, on_delete=models.CASCADE)

    def __str__(self):
        return self.category
