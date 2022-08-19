from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(CategoryModel)
class CategoryTranslationOption(TranslationOptions):
    fields = ('title',)


@register(ProductModel)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', )
