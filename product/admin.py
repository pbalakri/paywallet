from django.contrib import admin

from .models import Product, ProductAdmin, DietaryRestriction, Category, CategoryAdmin, Dashboard, DashboardAdmin, DietaryRestrictionAdmin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin


@admin.register(Category)
class CategoryAdminTranslationOptions(CategoryAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Product)
class ProductAdminTranslationOptions(ProductAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(DietaryRestriction)
class DietaryRestrictionAdminTranslationOptions(DietaryRestrictionAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


# admin.site.register(Product)
# admin.site.register(DietaryRestriction)
# admin.site.register(Category)
admin.site.register(Dashboard, DashboardAdmin)
