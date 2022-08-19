from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


from .models import *


class MyTranslation(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(CategoryModel)
class CategoryModelAdmin(MyTranslation):
    list_display = ['title', 'created_at']
    list_filter = ['created_at', ]
    search_fields = ['title']


class ProductImageModelAdmin(admin.StackedInline):
    model = ProductImageModel



@admin.register(ProductModel)
class ProductModelAdmin(MyTranslation):
    list_display = ['title', 'price', 'discount','created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title']
    autocomplete_fields = ['category']
    readonly_fields = ['real_price']
    inlines = [ProductImageModelAdmin]


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at', ]
    search_fields = ['title']