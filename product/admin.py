from django.contrib import admin

from .models import Product, ProductAdmin, Category, CategoryAdmin, Dashboard, DashboardAdmin, Allergy
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin


@admin.register(Category)
class CategoryAdminTranslationOptions(CategoryAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Product)
class ProductAdminTranslationOptions(ProductAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Allergy)
class AllergyAdminTranslationOptions(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Dashboard, DashboardAdmin)
