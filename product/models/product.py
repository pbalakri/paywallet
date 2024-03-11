from django.db import models
import uuid
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationTabularInline
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from paywallet.storage_backends import PublicMediaStorage
from django.utils.html import format_html
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
        permissions = [('import_product', 'Can import Products'),
                       ('export_product', 'Can export Products')]


class ProductResource(resources.ModelResource):
    category_name = fields.Field(
        column_name='category_name',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name'))

    class Meta:
        model = Product
        fields = ('id', 'name', 'description',
                  'category_name')
        import_id_fields = ('id',)


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'image', 'category', 'all_allergies')
    fields = ('name', 'image', 'category', 'allergies')
    search_fields = ('name',)

    def thumbnail(self, obj):
        try:
            return format_html('<img src="{}" style="width: 40px; \
                           height: 40px"/>'.format(obj.image.url))
        except:
            return None

    def all_allergies(self, obj):
        return ", ".join([p.name for p in obj.allergies.all()])


class ProductInlines(TranslationTabularInline):
    model = Product
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInlines]
    search_fields = ('name',)
