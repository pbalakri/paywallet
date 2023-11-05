from django.db import models
import uuid
from django.contrib import admin

from .school import School


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


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


class ProductAdmin(admin.ModelAdmin):
    fields = (('name', 'image'), 'description', ('price', 'stock'),
              ('category', 'is_active'), 'school')
    search_fields = ('name',)

    def all_restrictions(self, obj):
        return ", ".join([p.name for p in obj.restriction.all()])
