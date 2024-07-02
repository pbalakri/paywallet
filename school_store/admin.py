from django.contrib import admin

from .models import Product, ProductAdmin, Category, CategoryAdmin, Order, OrderAdmin, SchoolOrder, SchoolOrderAdmin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin


@admin.register(Category)
class CategoryAdminTranslationOptions(CategoryAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Product)
class ProductAdminTranslationOptions(ProductAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Order, OrderAdmin)
admin.site.register(SchoolOrder, SchoolOrderAdmin)
