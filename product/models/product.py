from django.db import models
import uuid
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationTabularInline

from paywallet.storage_backends import PublicMediaStorage

from .allergy import Allergy


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        'self', on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        storage=PublicMediaStorage(), upload_to='products/', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, blank=True, null=True)
    allergies = models.ManyToManyField(Allergy, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'category', 'all_allergies')
    fields = ('name', 'image', 'category', 'allergies')
    search_fields = ('name',)

    def all_allergies(self, obj):
        return ", ".join([p.name for p in obj.allergies.all()])


class ProductInlines(TranslationTabularInline):
    model = Product
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInlines]
    search_fields = ('name',)
