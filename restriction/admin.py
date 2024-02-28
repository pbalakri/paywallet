from django.contrib import admin

# Register your models here.
from .models import PaymentRestriction, CategoryRestriction, DietRestriction, ProductRestriction, PaymentRestrictionAdmin
admin.site.register(PaymentRestriction, PaymentRestrictionAdmin)
admin.site.register(CategoryRestriction)
admin.site.register(DietRestriction)
admin.site.register(ProductRestriction)
