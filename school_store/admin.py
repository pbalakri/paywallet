from django.contrib import admin

from .models import Product, ProductAdmin, Category, CategoryAdmin, Order, OrderAdmin

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
