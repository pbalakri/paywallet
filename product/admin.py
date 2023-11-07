from django.contrib import admin

from .models import Product, ProductAdmin, DietaryRestriction, Category, CategoryAdmin
admin.site.register(Product, ProductAdmin)
admin.site.register(DietaryRestriction)
admin.site.register(Category, CategoryAdmin)
