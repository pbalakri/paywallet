from django.contrib import admin

from .models import Product, ProductAdmin, Category, CategoryAdmin

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
