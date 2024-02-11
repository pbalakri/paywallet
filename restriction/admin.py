from django.contrib import admin

# Register your models here.
from .models import PaymentRestriction, CategoryRestriction, DietRestriction
admin.site.register(PaymentRestriction)
admin.site.register(CategoryRestriction)
admin.site.register(DietRestriction)
