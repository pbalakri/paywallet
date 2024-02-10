from django.contrib import admin

from .models import Product, ProductAdmin, Category, CategoryAdmin, Order, OrderAdmin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin


@admin.register(Category)
class CategoryAdminTranslationOptions(CategoryAdmin, TabbedExternalJqueryTranslationAdmin):
    pass


@admin.register(Product)
class ProductAdminTranslationOptions(ProductAdmin, TabbedExternalJqueryTranslationAdmin):
    pass


# admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
