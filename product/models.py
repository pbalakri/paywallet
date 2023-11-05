from django.db import models
import uuid
from django.contrib import admin


class Product(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', blank=True)
    restriction = models.ManyToManyField('DietaryRestriction', blank=True)

    def __str__(self):
        return self.name


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'all_restrictions')
    fields = ('name', 'image', 'restriction')
    search_fields = ('name',)

    def all_restrictions(self, obj):
        return ", ".join([p.name for p in obj.restriction.all()])


class DietaryRestriction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
