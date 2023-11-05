from django.contrib import admin

from .models import Product, ProductAdmin, DietaryRestriction
admin.site.register(Product, ProductAdmin)
admin.site.register(DietaryRestriction)
