from django.contrib import admin

from .models import Product, ProductAdmin, DietaryRestriction, Category, CategoryAdmin, Dashboard, DashboardAdmin, DietaryRestrictionAdmin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin


@admin.register(Category)
class CategoryAdminTranslationOptions(CategoryAdmin, TabbedExternalJqueryTranslationAdmin):
    pass


@admin.register(Product)
class ProductAdminTranslationOptions(ProductAdmin, TabbedExternalJqueryTranslationAdmin):
    pass


@admin.register(DietaryRestriction)
class DietaryRestrictionAdminTranslationOptions(DietaryRestrictionAdmin, TabbedExternalJqueryTranslationAdmin):
    pass


# admin.site.register(Product)
# admin.site.register(DietaryRestriction)
# admin.site.register(Category)
admin.site.register(Dashboard, DashboardAdmin)
