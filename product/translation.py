from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Allergy


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'ar')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'ar')


@register(Allergy)
class AllergyTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'ar')
