from django.contrib import admin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

# Register your models here.
from .models import PaymentRestriction, CategoryRestriction, DietRestriction, ProductRestriction
admin.site.register(PaymentRestriction)
admin.site.register(CategoryRestriction)
admin.site.register(DietRestriction)
admin.site.register(ProductRestriction)
