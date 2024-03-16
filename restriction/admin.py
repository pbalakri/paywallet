from django.contrib import admin

# Register your models here.
from .models import PaymentRestriction, CategoryRestriction, CategoryRestrictionAdmin, DietRestriction, DietRestrictionAdmin, ProductsRestriction, ProductsRestrictionAdmin, PaymentRestrictionAdmin
admin.site.register(PaymentRestriction, PaymentRestrictionAdmin)
admin.site.register(CategoryRestriction, CategoryRestrictionAdmin)
admin.site.register(DietRestriction, DietRestrictionAdmin)
admin.site.register(ProductsRestriction, ProductsRestrictionAdmin)
