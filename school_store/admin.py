from django.contrib import admin

from .models import Product, ProductAdmin, Category, CategoryAdmin, Order, OrderAdmin
from modeltranslation.admin import TranslationAdmin


@admin.register(Category)
class CategoryAdminTranslationOptions(CategoryAdmin, TranslationAdmin):
    pass


admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
