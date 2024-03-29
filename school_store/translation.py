from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'ar')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'ar')
